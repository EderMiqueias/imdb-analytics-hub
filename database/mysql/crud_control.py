import mysql.connector
from mysql.connector import Error

from database.migrations.db_base import BaseCRUD


class MySQLCRUD(BaseCRUD):
    def __init__(self, host, database, user, password, port):
        """Inicializa a conexão com o banco de dados MySQL"""
        super().__init__(host, database, user, password, port)

    def connect(self):
        """Estabelece a conexão com o banco de dados"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if self.connection.is_connected():
                print("Conexão ao MySQL estabelecida com sucesso")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão ao MySQL encerrada")

    def execute_query(self, query: str, params=None, fetch=False):
        """Executa uma query genérica no banco de dados"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if fetch:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount
            cursor.close()
            return result

        except Error as e:
            print(f"Erro ao executar query: {e}")
            self.connection.rollback()
            return None

    def insert(self, table: str, data: dict):
        """Insere um novo registro na tabela especificada"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        rows_affected = self.execute_query(query, tuple(data.values()))
        return rows_affected

    def executemany(self, query, values):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.executemany(query, values)
            cursor.close()
            self.connection.commit()
        except Error as e:
            self.connection.rollback()
            print(f"Erro ao executar query: {e}")

    def select(self, table: str, columns: str='*', where: str=None, params=None):
        """Realiza uma consulta na tabela especificada"""
        query = f"SELECT {columns} FROM {table}"
        if where:
            query += f" WHERE {where}"

        result = self.execute_query(query, params, fetch=True)
        return result

    def update(self, table: str, data: dict, where: str, params=None):
        """Atualiza registros na tabela especificada"""
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"

        # Combina os valores do data com os parâmetros adicionais
        values = tuple(data.values()) + (tuple(params) if params else ())

        rows_affected = self.execute_query(query, values)
        return rows_affected

    def delete(self, table: str, where: str, params=None):
        """Remove registros da tabela especificada"""
        query = f"DELETE FROM {table} WHERE {where}"

        rows_affected = self.execute_query(query, params)
        return rows_affected

    def __del__(self):
        """Destrutor que fecha a conexão quando o objeto é destruído"""
        self.disconnect()


def create_mysql_crud_service() -> MySQLCRUD:
    from config import MySQLConfig as c

    return MySQLCRUD(
        host=c.HOST,
        database=c.DATABASE,
        password=c.PASSWORD,
        user=c.USER,
        port=c.PORT
    )
