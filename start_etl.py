from etl import *
from database import create_mysql_crud_service


if __name__ == "__main__":
    mysql_service = create_mysql_crud_service()
    dfs = carregar_dfs_from_tsvs()

    carregar_dim_titulo(mysql_service, dfs)
    carregar_dim_pessoa(mysql_service, dfs)
    carregar_dim_tempo(mysql_service, dfs)
    carregar_dim_papel(mysql_service, dfs)
    print("ETL concluído com sucesso.")