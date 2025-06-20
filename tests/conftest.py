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

@pytest.fixture(scope="function")
def cinemas_data(create_address):
    return [
        {
            "nome": "Cinema Exemplo",
            "cnpj": "12.345.678/0001-90",
            "telefone": "1234567890",
            "email": "cinema@gmail.com",
            "ativo": True,
            "endereco_id": create_address["id"]
        },
        {
            "nome": "Cinema Exemplo 2",
            "cnpj": "12.345.678/0001-94",
            "telefone": "1234567890",
            "email": "cinema2@gmail.com",
            "ativo": True,
            "endereco_id": create_address["id"]
        },
    ]

@pytest.fixture(scope="function")
def create_cinema(client, cinema_data):
    response = client.post("/api/v1/cinema", json=cinema_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

@pytest.fixture(scope="function")
def create_cinemas(client, cinemas_data):
    created_cinemas = []
    for cinema in cinemas_data:
        response = client.post("/api/v1/cinema", json=cinema)
        assert response.status_code == status.HTTP_201_CREATED
        created_cinemas.append(response.json())
    return created_cinemas

@pytest.fixture(scope="function")
def product_payload(create_cinema):
    return {
        "nome": "Produto Exemplo",
        "descricao": "Descrição do produto exemplo",
        "categoria": "Doces",
        "preco": 19.99,
        "imagem_url": "http://example.com/imagem.jpg",
        "disponivel": True,
        "cinema_id": create_cinema["id"]
    }

@pytest.fixture(scope="function")
def create_product(client, product_payload):
    response = client.post("/api/v1/products", json=product_payload)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()