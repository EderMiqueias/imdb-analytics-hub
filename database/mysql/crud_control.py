import mysql.connector
from mysql.connector import Error


class MySQLCRUD:
    def __init__(self, host, database, user, password):
        """Inicializa a conexão com o banco de dados MySQL"""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):
        """Estabelece a conexão com o banco de dados"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
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
                return result
            else:
                self.connection.commit()
                return cursor.rowcount

        except Error as e:
            print(f"Erro ao executar query: {e}")
            self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def insert(self, table: str, data: dict):
        """Insere um novo registro na tabela especificada"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        rows_affected = self.execute_query(query, tuple(data.values()))
        return rows_affected

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
