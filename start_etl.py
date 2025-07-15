from etl import *
from database import create_mysql_crud_service


def etl_dimensoes(service, dfs):
    carregar_dim_titulo(service, dfs)
    carregar_dim_pessoa(service, dfs)
    carregar_dim_tempo(service, dfs)
    carregar_dim_papel(service, dfs)


def etl_fatos(service, dfs):
    carregar_fato_avaliacao_titulo(service, dfs)
    carregar_fato_pessoa(service, dfs)


if __name__ == "__main__":
    mysql_service = create_mysql_crud_service()
    loaded_dfs = carregar_dfs_from_tsvs()

    etl_dimensoes(mysql_service, loaded_dfs)
    etl_fatos(mysql_service, loaded_dfs)

    print("ETL concluído com sucesso.")
