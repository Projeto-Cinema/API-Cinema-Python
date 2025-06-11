from re import M
from typing import Dict, List
from venv import create
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

class TestUsuarioGetByCPF:

    @pytest.fixture
    def usuario_data(self):
        return {
            "nome": "Wesley",
            "email": "wesley@gmail.com",
            "cpf": "12345678901",
            "senha": "senha123",
            "telefone": "1234567890"
        }
    
    @pytest.fixture
    def create_user(self, client, usuario_data):
        response = client.post("api/v1/Users", json=usuario_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    def test_get_user_by_cpf_integration_success(self, client, create_user):
        user_cpf = create_user["cpf"]

        response = client.get(f"/api/v1/Users/cpf/{user_cpf}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == create_user["id"]
        assert response_data["nome"] == create_user["nome"]
        assert response_data["email"] == create_user["email"]
        assert response_data["cpf"] == user_cpf
        assert response_data["telefone"] == create_user["telefone"]

class TestUsuarioGetAll:

    @pytest.fixture(scope="class")
    def usuarios_data(self) -> List[Dict]:
        return [
            {"nome": "wesley", "email": "wesley@gmail.com", "cpf": "1111111111", "senha": "senha123", "telefone": "1234567890", "tipo": "cliente", "ativo": True},
            {"nome": "maria", "email": "maria@gmail.com", "cpf": "2222222222", "senha": "senha123", "telefone": "0987654321", "tipo": "cliente", "ativo": True},
            {"nome": "joao", "email": "joao@gmail.com", "cpf": "3333333333", "senha": "senha123", "telefone": "1122334455", "tipo": "cliente", "ativo": False},
        ]

    @pytest.fixture()
    def create_users(self, client, usuarios_data: List[Dict]):
        for user_data in usuarios_data:
            response = client.post("api/v1/Users", json=user_data)
            assert response.status_code == status.HTTP_201_CREATED

    def test_list_all_users_without_filters(self, client, usuarios_data: List[Dict], create_users):
        response = client.get("api/v1/Users")

        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == len(usuarios_data)

class TestUsuarioUpdate:

    @pytest.fixture
    def usuario_data(self):
        return {
            "nome": "Wesley",
            "email": "weslin@gmail.com",
            "cpf": "12345678901",
            "senha": "senha123",
            "telefone": "1234567890",
        }
    
    @pytest.fixture
    def create_user(self, client, usuario_data):
        response = client.post("api/v1/Users", json=usuario_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    def test_update_user_integration_success(self, client, create_user):
        user_id = create_user["id"]

        response = client.put(f"/api/v1/Users/{user_id}", json={
            "nome": "Wesley Updated",
            "email": "weslin@gmail.com",
            "cpf": "11111111111",
            "senha": "newpassword123",
            "telefone": "0987654321"
        })

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == user_id
        assert response_data["nome"] == "Wesley Updated"
        assert response_data["nome"] != create_user["nome"]
        assert response_data["email"] == create_user["email"]

class TestUsuarioDelete:

    @pytest.fixture
    def usuario_data(self):
        return {
            "nome": "Wesley",
            "email": "weslin@gmail.com",
            "cpf": "12345678901",
            "senha": "senha123",
            "telefone": "1234567890",
        }
    
    @pytest.fixture
    def create_user(self, client, usuario_data):
        response = client.post("api/v1/Users", json=usuario_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    def test_delete_user_partial_integration_success(self, client, create_user):
        user_id = create_user["id"]

        response_delete = client.delete(f"/api/v1/Users/{user_id}")

        assert response_delete.status_code == status.HTTP_204_NO_CONTENT

        response_get = client.get(f"/api/v1/Users/{user_id}")
        response_data_get = response_get.json()
        assert response_data_get["ativo"] is False

class TestUsuarioPermanentDelete:

    @pytest.fixture
    def usuario_data(self):
        return {
            "nome": "Wesley",
            "email": "weslin@gmail.com",
            "cpf": "12345678901",
            "senha": "senha123",
            "telefone": "1234567890",
        }
    
    @pytest.fixture
    def create_user(self, client, usuario_data):
        response = client.post("api/v1/Users", json=usuario_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    def test_delete_user_permanent_integration_success(self, client, create_user):
        user_id = create_user["id"]

        response_delete = client.delete(f"/api/v1/Users/delete/{user_id}")

        assert response_delete.status_code == status.HTTP_204_NO_CONTENT

        response_get = client.get(f"/api/v1/Users/{user_id}")
        assert response_get.status_code == status.HTTP_404_NOT_FOUND

class TestUsuarioDeactivate:

    @pytest.fixture
    def usuario_data(self):
        return {
            "nome": "Wesley",
            "email": "weslin@gmail.com",
            "cpf": "12345678901",
            "senha": "senha123",
            "ativo": True,
            "telefone": "1234567890",
        }
    
    @pytest.fixture
    def create_user(self, client, usuario_data):
        response = client.post("api/v1/Users", json=usuario_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    def test_deactivate_user_integration_success(self, client, create_user):
        user_id = create_user["id"]

        response = client.patch(f"/api/v1/Users/{user_id}/deactivate")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == user_id
        assert response_data["ativo"] is False
