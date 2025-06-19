import pytest

from fastapi import status

class TestCinemaController:

    @pytest.fixture
    def cinema_data(self):
        return {
            "nome": "Cinema Exemplo",
            "cnpj": "12.345.678/0001-90",
            "telefone": "1234567890",
            "email": "cinema@gmail.com",
            "ativo": True,
            "endereco_id": 1
        }
    
    def test_create_cinema_integration_success(self, client, cinema_data):
        response = client.post("/api/v1/cinema", json=cinema_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["nome"] == cinema_data["nome"]
        assert response_data["cnpj"] == cinema_data["cnpj"]
        assert response_data["endereco_id"] == cinema_data["endereco_id"]