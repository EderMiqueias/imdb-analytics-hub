import pandas as pd

from pathlib import Path
from datetime import datetime

from DTO import DFs
from database.migrations.db_base import BaseCRUD
from utils.dates import diferenca_entre_datetimes

# Caminho base para os arquivos .tsv
BASE_PATH = Path("tsv_input_files")


def carregar_dim_titulo(service: BaseCRUD):
    start_time = datetime.now()
    df = pd.read_csv(BASE_PATH / "title.basics.tsv", sep='\t', na_values='\\N', low_memory=False)
    df = df[pd.to_numeric(df['startYear'], errors='coerce') >= ANO_MINIMO]
    df = df[['tconst', 'titleType', 'primaryTitle', 'genres', 'runtimeMinutes']]
    print('Leitura de TSVs concluida.')
    diferenca_entre_datetimes(start_time, datetime.now())

    dados = []
    for _, row in df.iterrows():
        dados.append((
            int(row['tconst'][2:]),
            row['titleType'],
            row['primaryTitle'],
            row['genres'],
            int(row['runtimeMinutes']) if pd.notna(row['runtimeMinutes']) else None
        ))

    print("Iniciada a inserção na tabela DIM_Titulo")
    service.executemany("""
        INSERT INTO DIM_Titulo (pk_titulo, titleType, primaryTitle, genres, runtimeMinutes)
        VALUES (%s, %s, %s, %s, %s)
    """, dados)
    print(f"{len(dados)} registros inseridos em DIM_Titulo.")


def carregar_dim_pessoa(service: BaseCRUD):
    start_time = datetime.now()
    basics_df = pd.read_csv(BASE_PATH / "title.basics.tsv", sep='\t', na_values='\\N', low_memory=False)
    principals_df = pd.read_csv(BASE_PATH / "title.principals.tsv", sep='\t', na_values='\\N', low_memory=False)
    names_df = pd.read_csv(BASE_PATH / "name.basics.tsv", sep='\t', na_values='\\N', low_memory=False)

    print('Leitura de TSVs concluida.')
    diferenca_entre_datetimes(start_time, datetime.now())

    basics_df = basics_df[pd.to_numeric(basics_df['startYear'], errors='coerce') >= ANO_MINIMO]
    valid_tconsts = set(basics_df['tconst'])

    filtered_principals = principals_df[principals_df['tconst'].isin(valid_tconsts)]
    valid_nconsts = set(filtered_principals['nconst'])

    filtered_names = names_df[names_df['nconst'].isin(valid_nconsts)][['nconst', 'primaryName']].dropna()

    print('Filtragem de dados concluida.')
    diferenca_entre_datetimes(start_time, datetime.now())

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

    print('Limpeza de dados concluida.')
    diferenca_entre_datetimes(start_time, datetime.now())

    service.executemany("""
        INSERT INTO DIM_Pessoa (pk_pessoa, primaryName)
        VALUES (%s, %s)
    """, dados)
    print(f"{len(dados)} registros inseridos em DIM_Pessoa.")
    print('Inserção em DIM_Pessoa concluida.')
    diferenca_entre_datetimes(start_time, datetime.now())


def carregar_dim_tempo(service: BaseCRUD):
    df = pd.read_csv(BASE_PATH / "title.basics.tsv", sep='\t', na_values='\\N')
    df = df[pd.to_numeric(df['startYear'], errors='coerce') >= ANO_MINIMO]
    anos = df['startYear'].dropna().unique()
    for ano in anos:
        service.execute_query(
            """
                INSERT IGNORE INTO DIM_Tempo (pk_tempo, starYear)
                VALUES (%s, %s)
            """,
            (int(ano), int(ano)))


def carregar_dim_papel(service: BaseCRUD):
    # Lê arquivos
    basics_df = pd.read_csv(BASE_PATH / "title.basics.tsv", sep='\t', na_values='\\N', low_memory=False)
    principals_df = pd.read_csv(BASE_PATH / "title.principals.tsv", sep='\t', na_values='\\N', low_memory=False)

    # Filtra títulos dos últimos 3 anos
    basics_df = basics_df[pd.to_numeric(basics_df['startYear'], errors='coerce') >= ANO_MINIMO]

    # Junta títulos com papéis (título ↔ papel)
    valid_tconsts = set(basics_df['tconst'])
    filtered_principals = principals_df[principals_df['tconst'].isin(valid_tconsts)]

    # Remove duplicatas e valores nulos
    filtered_principals = filtered_principals[['category', 'characters']].drop_duplicates().fillna("NULL")

    dados = [(row['category'], row['characters']) for _, row in filtered_principals.iterrows()]

    print("Iniciada a inserção na tabela DIM_Papel")
    service.executemany("""
        INSERT INTO DIM_Papel (category, characters)
        VALUES (%s, %s)
    """, dados)
    print(f"{len(dados)} registros inseridos em DIM_Papel (últimos 3 anos).")

