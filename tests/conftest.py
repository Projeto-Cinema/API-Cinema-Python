from re import M
from fastapi.testclient import TestClient
from fastapi import status

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.genero import Genero
from app.models.schemas.enum.enum_util import StatusSalaEnum
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
def products_data(create_cinema):
    return [
        {
            "nome": "Produto Exemplo 1",
            "descricao": "Descrição do produto exemplo 1",
            "categoria": "Doces",
            "preco": 19.99,
            "imagem_url": "http://example.com/imagem1.jpg",
            "disponivel": True,
            "cinema_id": create_cinema["id"]
        },
        {
            "nome": "Produto Exemplo 2",
            "descricao": "Descrição do produto exemplo 2",
            "categoria": "Bebidas",
            "preco": 9.99,
            "imagem_url": "http://example.com/imagem2.jpg",
            "disponivel": True,
            "cinema_id": create_cinema["id"]
        }
    ]

@pytest.fixture(scope="function")
def create_product(client, product_payload):
    response = client.post("/api/v1/products", json=product_payload)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

@pytest.fixture(scope="function")
def create_products(client, products_data):
    created_products = []
    for product in products_data:
        response = client.post("/api/v1/products", json=product)
        assert response.status_code == status.HTTP_201_CREATED
        created_products.append(response.json())
    return created_products

@pytest.fixture(scope="function")
def sala_data(create_cinema):
    return {
        "nome": "Sala A1",
        "capacidade": 100,
        "tipo": "IMAX",
        "recursos": '{"projetor": "4K", "som": "Dolby Atmos"}',
        "mapa_assentos": '{"A": [1, 2, 3], "B": [1, 2, 3]}',
        "status": StatusSalaEnum.ATIVA,
        "cinema_id": create_cinema["id"]
    }

@pytest.fixture(scope="function")
def salas_data(create_cinema):
    return [
        {
            "nome": "Sala A1",
            "capacidade": 100,
            "tipo": "IMAX",
            "recursos": '{"projetor": "4K", "som": "Dolby Atmos"}',
            "mapa_assentos": '{"A": [1, 2, 3], "B": [1, 2, 3]}',
            "status": StatusSalaEnum.ATIVA,
            "cinema_id": create_cinema["id"]
        },
        {
            "nome": "Sala B1",
            "capacidade": 150,
            "tipo": "3D",
            "recursos": '{"projetor": "HD", "som": "Surround"}',
            "mapa_assentos": '{"A": [1, 2, 3], "B": [1, 2, 3]}',
            "status": StatusSalaEnum.INATIVO,
            "cinema_id": create_cinema["id"]
        }
    ]

@pytest.fixture(scope="function")
def create_sala(client, sala_data):
    response = client.post("/api/v1/room", json=sala_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

@pytest.fixture(scope="function")
def create_rooms(client, salas_data):
    created_rooms = []
    for rooms in salas_data:
        response = client.post("/api/v1/room", json=rooms)
        assert response.status_code == status.HTTP_201_CREATED
        created_rooms.append(response.json())
    return created_rooms

@pytest.fixture(scope="function")
def create_generos(db_session):
    from app.models.genero import Genero
    
    genero1 = Genero(nome="Ação")
    genero2 = Genero(nome="Comédia")

    db_session.add_all([genero1, genero2])
    db_session.commit()

    db_session.refresh(genero1)
    db_session.refresh(genero2)

    return [genero1.id, genero2.id]

@pytest.fixture(scope="function")
def filme_data(create_generos):
    return {
        "titulo": "Filme exemplo",
        "titulo_original": "Original Example",
        "sinopse": "Sinopse do filme exemplo",
        "duracao_min": 120,
        "diretor": "Diretor Exemplo",
        "elenco": "Ator 1, Ator 2",
        "classificacao": "12 anos",
        "ano_lancamento": 2023,
        "em_cartaz": True,
        "generos_id": create_generos,
    }

@pytest.fixture(scope="function")
def filmes_data(create_generos):
    return [
        {
            "titulo": "Filme exemplo",
            "titulo_original": "Original Example",
            "sinopse": "Sinopse do filme exemplo",
            "duracao_min": 120,
            "diretor": "Diretor Exemplo",
            "elenco": "Ator 1, Ator 2",
            "classificacao": "12 anos",
            "ano_lancamento": 2023,
            "em_cartaz": True,
            "generos_id": create_generos,
        },
        {
            "titulo": "Filme exemplo 2",
            "titulo_original": "Original Example 2",
            "sinopse": "Sinopse do filme exemplo 2",
            "duracao_min": 90,
            "diretor": "Diretor Exemplo 2",
            "elenco": "Ator 3, Ator 4",
            "classificacao": "14 anos",
            "ano_lancamento": 2022,
            "em_cartaz": False,
            "generos_id": create_generos,
        }
    ]

@pytest.fixture(scope="function")
def create_movie(client, filme_data):
    response = client.post("/api/v1/movies", json=filme_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

@pytest.fixture(scope="function")
def create_movies(client, filmes_data):
    created_movies = []
    for movie in filmes_data:
        response = client.post("/api/v1/movies", json=movie)
        assert response.status_code == status.HTTP_201_CREATED
        created_movies.append(response.json())
    return created_movies