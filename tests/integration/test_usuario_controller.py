import pytest

from fastapi import status

class TestUsuarioController:

    @pytest.fixture
    def usuario_data(self):
        return {
            "nome": "Wesley",
            "email": "wesley@gmail.com",
            "senha": "senha123",
            "telefone": "1234567890"
        }
    
    def test_create_user_integration(self, client, usuario_data):
        response = client.post("api/v1/Users", json=usuario_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["nome"] == usuario_data["nome"]
        assert response_data["email"] == usuario_data["email"]
        assert response_data["telefone"] == usuario_data["telefone"]

    def test_create_user_validation_error(self, client):
        invalid_data = {
            "nome": "",
            "email": "invalid-email",
        }

        response = client.post("api/v1/Users", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_duplicate_email(self, client, usuario_data):
        response1 = client.post("api/v1/Users", json=usuario_data)
        assert response1.status_code == status.HTTP_201_CREATED

        response2 = client.post("api/v1/Users", json=usuario_data)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

class TestUsuarioGetByID:

    @pytest.fixture
    def usuario_data(self):
        return {
            "nome": "Wesley",
            "email": "wesley@gmail.com",
            "senha": "senha123",
            "telefone": "1234567890"
        }
    
    @pytest.fixture
    def create_user(self, client, usuario_data):
        response = client.post("api/v1/Users", json=usuario_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    def test_get_user_by_id_integration_success(self, client, create_user):
        user_id = create_user["id"]

        response = client.get(f"/api/v1/Users/{user_id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == user_id
        assert response_data["nome"] == create_user["nome"]
        assert response_data["email"] == create_user["email"]
        assert response_data["telefone"] == create_user["telefone"]

class TestUsuarioGetByEmail:

    @pytest.fixture
    def usuario_data(self):
        return {
            "nome": "Wesley",
            "email": "wesley@gmail.com",
            "senha": "senha123",
            "telefone": "1234567890"
        }
    
    @pytest.fixture
    def create_user(self, client, usuario_data):
        response = client.post("api/v1/Users", json=usuario_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    def test_get_user_by_email_integration_success(self, client, create_user):
        user_email = create_user["email"]

        response = client.get(f"/api/v1/Users/email/{user_email}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == create_user["id"]
        assert response_data["nome"] == create_user["nome"]
        assert response_data["email"] == user_email
        assert response_data["telefone"] == create_user["telefone"]