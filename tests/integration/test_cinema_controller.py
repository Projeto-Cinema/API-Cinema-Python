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