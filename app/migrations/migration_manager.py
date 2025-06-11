import logging
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class MigrationManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(self.database_url)
        self.migrations_dir = Path(__file__).parent

    def create_migration_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS migrations_applied (
            id SERIAL PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """

        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
                logger.info("Tabela de controle de migrations criada")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar tabela de migrations: {e}")
            raise

    def get_applied_migrations(self):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT migration_name FROM migrations_applied"))
                return {row[0] for row in result.fetchall()}
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar migrations aplicadas: {e}")
            return set()
        
    def get_migration_files(self):
        sql_files = []
        for file_path in self.migrations_dir.glob("*.sql"):
            if file_path.is_file():
                sql_files.append(file_path.name)

        return sorted(sql_files)
    
    def execute_migration(self, migration_file: str):
        file_path = self.migrations_dir / migration_file

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()

            with self.engine.connect() as conn:
                conn.execute(text(sql_content))

                conn.execute(
                    text("INSERT INTO migrations_applied (migration_name) VALUES (:name)"),
                    {"name": migration_file}
                )
                conn.commit()
            
            logger.info(f"Migration '{migration_file}' executada com sucesso")

        except Exception as e:
            logger.error(f"Erro ao executar migration '{migration_file}': {e}")
            raise

    def run_migrations(self):
        logger.info("Iniciando processo de migrations...")

        self.create_migration_table()

        applied_migrations = self.get_applied_migrations()

        migration_files = self.get_migration_files()

        if not migration_files:
            logger.info("Nenhuma migration encontrada")
            return
        
        pending_migrations = [f for f in migration_files if f not in applied_migrations]

        if not pending_migrations:
            logger.info("Todas as migrations já foram aplicadas")
            return
        
        for migration_file in pending_migrations:
            try:
                self.execute_migration(migration_file)
            except Exception as e:
                logger.error(f"Falha na migration '{migration_file}'. Parando execução.")
                raise

        logger.info("Todas as migrations pendentes foram aplicadas com sucesso")