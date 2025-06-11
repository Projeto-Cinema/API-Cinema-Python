from fastapi.testclient import TestClient
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