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
    # return DFs(basics_df, [], [], [])


def carregar_dim_titulo(service: BaseCRUD, dfs: DFs):
    print("Carregando DIM_Titulo...")

    df = dfs.basics_df
    df = df[pd.to_numeric(df['startYear'], errors='coerce') >= ANO_MINIMO]

    df = df[['tconst', 'titleType', 'primaryTitle', 'genres', 'runtimeMinutes']].dropna(subset=['tconst', 'primaryTitle'])
    df = df[df['tconst'].str.match(r'tt\d+')]
    df = df.replace({pd.NA: None, float('nan'): None})

    dados = []
    for _, row in df.iterrows():
        dados.append((
            int(row['tconst'][2:]),
            row['titleType'],
            row['primaryTitle'],
            row['genres'],
            int(row['runtimeMinutes']) if pd.notna(row['runtimeMinutes']) else None
        ))

    service.executemany("""
        INSERT INTO DIM_Titulo (pk_titulo, titleType, primaryTitle, genres, runtimeMinutes)
        VALUES (%s, %s, %s, %s, %s)
    """, dados)
    print(f"\n{len(dados)} registros inseridos em DIM_Titulo.\n")


def carregar_dim_pessoa(service: BaseCRUD, dfs: DFs):
    start_time = datetime.now()
    basics_df = dfs.basics_df
    principals_df = dfs.principals_df
    names_df = dfs.names_df

    basics_df = basics_df[pd.to_numeric(basics_df['startYear'], errors='coerce') >= ANO_MINIMO]
    valid_tconsts = set(basics_df['tconst'])

    # filtered_principals = principals_df[principals_df['tconst'].isin(valid_tconsts)]
    # valid_nconsts = set(filtered_principals['nconst'])

    # filtered_names = names_df[names_df['nconst'].isin(valid_nconsts)][['nconst', 'primaryName']].dropna()
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
    print("Carregando DIM_Papel...")

    # basics_df = dfs.basics_df
    principals_df = dfs.principals_df

    # basics_df = basics_df[pd.to_numeric(basics_df['startYear'], errors='coerce') >= ANO_MINIMO]
    # valid_tconsts = set(basics_df['tconst'])

    # principals_df = principals_df[principals_df['tconst'].isin(valid_tconsts)]
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

