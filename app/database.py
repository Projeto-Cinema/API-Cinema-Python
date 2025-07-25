"""Module for database connection and initialization using SQLAlchemy and FastAPI."""

import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.migrations.migration_manager import MigrationManager

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Cria uma sessão de banco de dados para uso em rotas do FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_database():
    """Inicializa o banco de dados e executa as migrações."""
    try:
        migration_manager = MigrationManager(SQLALCHEMY_DATABASE_URL)
        migration_manager.run_migrations()

        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def create_tables():
    """Cria as tabelas no banco de dados usando SQLAlchemy."""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully:", list(Base.metadata.tables.keys()))
