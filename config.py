from os import environ

from dotenv import load_dotenv

load_dotenv()

class MySQLConfig:
    HOST = environ.get('MYSQL_HOST')
    PORT = environ.get('MYSQL_PORT')
    DATABASE = environ.get('MYSQL_DATABASE')
    USER = environ.get('MYSQL_USER')
    PASSWORD = environ.get('MYSQL_PASSWORD')

