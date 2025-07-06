from os import environ

from dotenv import load_dotenv

load_dotenv()

class MySQLConfig:
    HOST = environ.get('mysql_host')
    DATABASE = environ.get('mysql_database')
    USER = environ.get('mysql_user')
    PASSWORD = environ.get('mysql_password')
