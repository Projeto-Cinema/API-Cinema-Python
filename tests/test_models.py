import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocomit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Criar as tabelas

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.mark.skip(reason="Teste ainda não implementado")
def test_create_user(db_session):
    """Testa a criação de um usuário (ainda não implementado)"""


@pytest.mark.skip(reason="Teste ainda não implementado")
def test_update_user(db_session):
    """Testa a atualização de um usuário (ainda não implementado)"""


@pytest.mark.skip(reason="Teste ainda não implementado")
def test_delete_user(db_session):
    """Testa a deleção de um usuário (ainda não implementado)"""
