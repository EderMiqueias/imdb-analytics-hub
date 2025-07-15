import pandas as pd

from pathlib import Path
from datetime import datetime

from DTO import DFs
from database.migrations.db_base import BaseCRUD
from utils.data import string_para_lista

# Caminho base para os arquivos .tsv
BASE_PATH = Path("tsv_input_files")
ANO_MINIMO = datetime.now().year - 3  # Últimos 3 anos


def carregar_dfs_from_tsvs() -> DFs:
    # len 11.762.396
    basics_df = pd.read_csv(BASE_PATH / "title.basics.tsv", sep='\t', na_values='\\N', low_memory=False)

    # len 93.469.663
    principals_df = pd.read_csv(BASE_PATH / "title.principals.tsv", sep='\t', na_values='\\N', low_memory=False)

    # len 14.535.473
    names_df = pd.read_csv(BASE_PATH / "name.basics.tsv", sep='\t', na_values='\\N', low_memory=False)

    # len 1.581.387
    ratings_df = pd.read_csv(BASE_PATH / "title.ratings.tsv", sep='\t', na_values='\\N', low_memory=False)

    return DFs(basics_df, principals_df, names_df, ratings_df)


def carregar_dim_titulo(service: BaseCRUD, dfs: DFs):
    print("📥 Carregando DIM_Titulo...")

    df = dfs.basics_df
    df = df[pd.to_numeric(df['startYear'], errors='coerce') >= ANO_MINIMO]

    df = df[['tconst', 'titleType', 'primaryTitle', 'genres', 'runtimeMinutes']].dropna(subset=['tconst', 'primaryTitle'])
    df = df[df['tconst'].str.match(r'tt\d+')]
    df = df.replace({pd.NA: None, float('nan'): None})

    dados = []
    for _, row in df.iterrows():
        try:
            pk = int(row['tconst'][2:])
            runtime = int(row['runtimeMinutes']) if pd.notna(row['runtimeMinutes']) else None
            dados.append((pk, row['titleType'], row['primaryTitle'], row['genres'], runtime))
        except:
            continue

    service.executemany("""
        INSERT INTO DIM_Titulo (pk_titulo, titleType, primaryTitle, genres, runtimeMinutes)
        VALUES (%s, %s, %s, %s, %s)
    """, dados)
    print(f"\n✅ {len(dados)} registros inseridos em DIM_Titulo.\n")


def carregar_dim_pessoa(service: BaseCRUD, dfs: DFs):
    names_df = dfs.names_df
    filtered_names = names_df[['nconst', 'primaryName']].dropna()

    # Remove nconsts malformados e nomes vazios
    filtered_names = filtered_names[
        filtered_names['nconst'].str.match(r'nm\d+') &
        filtered_names['primaryName'].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0)
    ]

    # Monta dados limpos
    dados = []
    for _, row in filtered_names.iterrows():
        try:
            pk = int(row['nconst'][2:])
            dados.append((pk, row['primaryName']))
        except:
            continue

    service.executemany("""
        INSERT INTO DIM_Pessoa (pk_pessoa, primaryName)
        VALUES (%s, %s)
    """, dados)
    print(f"\n✅ {len(dados)} registros inseridos em DIM_Pessoa.\n")


def carregar_dim_tempo(service: BaseCRUD, dfs: DFs):
    df = dfs.basics_df
    df = df[pd.to_numeric(df['startYear'], errors='coerce') >= ANO_MINIMO]
    anos = df['startYear'].dropna().unique()
    for ano in anos:
        service.execute_query(
            """
                INSERT IGNORE INTO DIM_Tempo (pk_tempo, starYear)
                VALUES (%s, %s)
            """,
            (int(ano), int(ano)))
    print(f"\n✅ {len(anos)} registros inseridos em DIM_Tempo.\n")


def carregar_dim_papel(service: BaseCRUD, dfs: DFs):
    print("📥 Carregando DIM_Papel...")

    principals_df = dfs.principals_df
    principals_df = principals_df[['category', 'characters']].dropna().drop_duplicates()

    dados = []
    for _, row in principals_df.iterrows():
        for character in string_para_lista(row['characters']):
            dados.append((str(row['category']), character))

    service.executemany("""
            INSERT INTO DIM_Papel (category, character_name)
            VALUES (%s, %s)
        """, dados)
    print(f"\n✅ {len(dados)} registros inseridos em DIM_Papel.\n")

def carregar_fato_avaliacao_titulo(service: BaseCRUD, dfs: DFs):
    print("📥 Carregando Fato_Avaliacao_Titulo...")

    basics_df = dfs.basics_df
    ratings_df = dfs.ratings_df

    basics_df = basics_df[pd.to_numeric(basics_df['startYear'], errors='coerce') >= ANO_MINIMO]
    basics_df = basics_df[basics_df['tconst'].str.match(r'tt\d+')]

    merged_df = pd.merge(basics_df[['tconst', 'startYear']], ratings_df, on='tconst')
    merged_df = merged_df.dropna(subset=['tconst', 'startYear', 'numVotes', 'averageRating'])

    dados = []
    for _, row in merged_df.iterrows():
        try:
            pk_titulo = int(row['tconst'][2:])
            pk_tempo = int(row['startYear'])
            votos = int(row['numVotes'])
            nota = float(row['averageRating'])
            dados.append((pk_titulo, pk_tempo, votos, nota))
        except:
            continue

    service.executemany("""
        INSERT INTO Fato_Avaliacao_Titulo (
            DIM_Titulo_pk_titulo,
            DIM_Tempo_pk_tempo,
            numVotes,
            averageRating
        ) VALUES (%s, %s, %s, %s)
    """, dados)
    print(f"✅ {len(dados)} registros inseridos em Fato_Avaliacao_Titulo.\n")


def carregar_fato_pessoa(service: BaseCRUD, dfs: DFs):
    print("📥 Carregando Fato_Pessoa...")

    basics_df = dfs.basics_df
    ratings_df = dfs.ratings_df
    principals_df = dfs.principals_df

    basics_df = basics_df[pd.to_numeric(basics_df['startYear'], errors='coerce') >= ANO_MINIMO]
    basics_df = basics_df[basics_df['tconst'].str.match(r'tt\d+')]
    valid_titles = set(basics_df['tconst'])

    merged = pd.merge(principals_df, ratings_df, on='tconst')
    merged = merged[merged['tconst'].isin(valid_titles)]
    merged = merged[merged['nconst'].str.match(r'nm\d+')]

    merged['pk_pessoa'] = merged['nconst'].apply(lambda x: int(x[2:]))
    merged['numVotes'] = pd.to_numeric(merged['numVotes'], errors='coerce')
    merged['averageRating'] = pd.to_numeric(merged['averageRating'], errors='coerce')

    merged = merged.dropna(subset=['pk_pessoa', 'numVotes', 'averageRating'])

    # Agrupamento por pessoa
    grupo = merged.groupby('pk_pessoa').apply(lambda g: pd.Series({
        'numTitulos': g['tconst'].nunique(),
        'totalVotes': g['numVotes'].sum(),
        'mediaPonderada': (g['averageRating'] * g['numVotes']).sum() / g['numVotes'].sum()
    })).reset_index()

    dados = [(
        int(row['pk_pessoa']),
        int(row['numTitulos']),
        int(row['totalVotes']),
        round(row['mediaPonderada'], 2)
    ) for _, row in grupo.iterrows()]

    service.executemany("""
        INSERT IGNORE INTO Fato_Pessoa (
            DIM_Pessoa_pk_pessoa,
            numTitulos,
            numVotes,
            averageRating
        ) VALUES (%s, %s, %s, %s)
    """, dados)
    print(f"✅ {len(dados)} registros inseridos em Fato_Pessoa.\n")
