class BaseCRUD:
    def __init__(self, host, database, user, password, port):
        """Inicializa a conexão com o banco de dados MySQL"""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.connect()

    def connect(self):
        """Estabelece a conexão com o banco de dados"""
        raise NotImplementedError('delete')

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        raise NotImplementedError('delete')

    def execute_query(self, query: str, params=None, fetch=False):
        """Executa uma query genérica no banco de dados"""
        raise NotImplementedError('delete')

    def insert(self, table: str, data: dict):
        """Insere um novo registro na tabela especificada"""
        raise NotImplementedError('delete')

    def select(self, table: str, columns: str='*', where: str=None, params=None):
        """Realiza uma consulta na tabela especificada"""
        raise NotImplementedError('delete')

    def update(self, table: str, data: dict, where: str, params=None):
        """Atualiza registros na tabela especificada"""
        raise NotImplementedError('delete')

    def delete(self, table: str, where: str, params=None):
        """Remove registros da tabela especificada"""
        raise NotImplementedError('delete')

    def __del__(self):
        """Destrutor que fecha a conexão quando o objeto é destruído"""
        self.disconnect()
