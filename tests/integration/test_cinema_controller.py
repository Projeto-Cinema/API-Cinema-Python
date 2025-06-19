from typing import Dict, List
import pytest

from fastapi import status

class TestCinemaController:

    def test_create_cinema_integration_success(self, client, cinema_data):
        response = client.post("/api/v1/cinema", json=cinema_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["nome"] == cinema_data["nome"]
        assert response_data["cnpj"] == cinema_data["cnpj"]
        assert response_data["endereco_id"] == cinema_data["endereco_id"]

    def test_create_cinema_duplicate_email(self, client, cinema_data):
        response1 = client.post("/api/v1/cinema", json=cinema_data)
        assert response1.status_code == status.HTTP_201_CREATED

        response2 = client.post("/api/v1/cinema", json=cinema_data)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

class TestCinemaControllerGetByID:

    def test_get_cinema_by_id_integration_success(self, client, create_cinema):
        cinema_id = create_cinema["id"]

        response = client.get(f"/api/v1/cinema/{cinema_id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == cinema_id
        assert response_data["nome"] == create_cinema["nome"]
        assert response_data["cnpj"] == create_cinema["cnpj"]
        assert response_data["endereco_id"] == create_cinema["endereco_id"]

    def test_get_cinema_by_id_not_found(self, client):
        response = client.get("/api/v1/cinema/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

class TestCinemaControllerGetByName:

    def test_get_cinema_by_name_integration_success(self, client, create_cinema):
        cinema_name = create_cinema["nome"]

        response = client.get(f"/api/v1/cinema/name/{cinema_name}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["nome"] == cinema_name
        assert response_data["cnpj"] == create_cinema["cnpj"]
        assert response_data["endereco_id"] == create_cinema["endereco_id"]

    def test_get_cinema_by_name_not_found(self, client):
        response = client.get("/api/v1/cinema/name/NonExistentCinema")

        assert response.status_code == status.HTTP_404_NOT_FOUND

class TestCinemaControllerGetAll:

    def test_get_all_cinemas_integration_success(self, client, cinemas_data: List[Dict], create_cinemas):
        response = client.get("/api/v1/cinema")

        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == len(cinemas_data)

class TestCinemaControllerUpdate:

    def test_update_cinema_integration_success(self, client, create_cinema, create_address):
        cinema_id = create_cinema["id"]

        response = client.put(f"/api/v1/cinema/{cinema_id}", json={
            "nome": "Cinema Updated",
            "cnpj": "12.345.678/0001-90",
            "telefone": "12345623213",
            "email": "cinemaupdated@gmail.com",
            "ativo": True,
            "endereco_id": create_address["id"]
        })

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == cinema_id
        assert response_data["nome"] == "Cinema Updated"
        assert response_data["nome"] != create_cinema["nome"]
        assert response_data["email"] == "cinemaupdated@gmail.com"