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