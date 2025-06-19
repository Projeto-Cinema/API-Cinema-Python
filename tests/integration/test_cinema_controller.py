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