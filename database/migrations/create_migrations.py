from database import create_mysql_crud_service
from utils.file import ler_arquivo

dimensional_migration_content = ler_arquivo('dimensional/mysql_migration.sql')
relational_migration_content = ler_arquivo('relational/mysql_migration.sql')

service = create_mysql_crud_service()

service.execute_query(dimensional_migration_content, fetch=True)
service.execute_query(relational_migration_content, fetch=True)

