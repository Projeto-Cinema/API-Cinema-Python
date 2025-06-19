from fastapi.testclient import TestClient
from fastapi import status

import pytest

from setuptools import find_packages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.database import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def test_app():
    app.dependency_overrides[get_db] = override_get_db
    return app

@pytest.fixture(scope="function")
def db_setup():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_app, db_setup):
    with TestClient(test_app) as test_client:
        yield test_client

@pytest.fixture
def db_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def endereco_payload():
    return {
        "cep": "12345678",
        "logradouro": "Rua Exemplo",
        "numero": 123,
        "bairro": "Bairro Exemplo",
        "cidade": "Cidade Exemplo",
        "estado": "EX",
        "complemento": "Apto 1",
        "referencia": "ref exemplo"
    }

@pytest.fixture(scope="function")
def create_address(client, endereco_payload):
    response = client.post("api/v1/address", json=endereco_payload)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

@pytest.fixture(scope="function")
def cinema_data(create_address):
    return {
        "nome": "Cinema Exemplo",
        "cnpj": "12.345.678/0001-90",
        "telefone": "1234567890",
        "email": "cinema@gmail.com",
        "ativo": True,
        "endereco_id": create_address["id"]
    }