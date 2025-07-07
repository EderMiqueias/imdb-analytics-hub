import pandas as pd
from pathlib import Path

from database.migrations.db_base import BaseCRUD


# Caminho base para os arquivos .tsv
BASE_PATH = Path("tsv_input_files")


def carregar_dim_titulo(service: BaseCRUD):
    df = pd.read_csv(BASE_PATH / "title.basics.tsv", sep='\t', na_values='\\N')
    df = df[['tconst', 'titleType', 'primaryTitle', 'genres', 'runtimeMinutes']]
    for _, row in df.iterrows():
        service.execute_query(
            """
                INSERT INTO DIM_Titulo (pk_titulo, titleType, primaryTitle, genres, runtimeMinutes)
                VALUES (%s, %s, %s, %s, %s)
            """,
            (
                int(row['tconst'][2:]),  # exemplo de conversão de 'tt0000001' -> 1
                row['titleType'],
                row['primaryTitle'],
                row['genres'],
                int(row['runtimeMinutes']) if not pd.isna(row['runtimeMinutes']) else None
            )
        )


def carregar_dim_pessoa(service: BaseCRUD):
    df = pd.read_csv(BASE_PATH / "name.basics.tsv", sep='\t', na_values='\\N')
    df = df[['nconst', 'primaryName']]
    for _, row in df.iterrows():
        service.execute_query(
            """
                INSERT INTO DIM_Pessoa (pk_pessoa, primaryName)
                VALUES (%s, %s)
            """,
            (
                int(row['nconst'][2:]),  # 'nm0000001' -> 1
                row['primaryName']
            )
        )


def carregar_dim_tempo(service: BaseCRUD):
    df = pd.read_csv(BASE_PATH / "title.basics.tsv", sep='\t', na_values='\\N')
    anos = df['startYear'].dropna().unique()
    for ano in anos:
        service.execute_query(
            """
                INSERT IGNORE INTO DIM_Tempo (pk_tempo, starYear)
                VALUES (%s, %s)
            """,
            (int(ano), int(ano)))


def carregar_dim_papel(service: BaseCRUD):
    df = pd.read_csv(BASE_PATH / "title.principals.tsv", sep='\t', na_values='\\N')
    df = df[['category', 'characters']].drop_duplicates()
    for idx, row in df.iterrows():
        service.execute_query(
            """
                INSERT INTO DIM_Papel (pk_papel, category, characters)
                VALUES (%s, %s, %s)
            """,
            (idx + 1, row['category'], row['characters']))
