import pytest

from fastapi import status

class TestCinemaController:

    @pytest.fixture
    def endereco_data(self):
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
    
    @pytest.fixture
    def create_address(self, client, endereco_data):
        response = client.post("api/v1/address", json=endereco_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    @pytest.fixture
    def cinema_data(self, create_address):
        return {
            "nome": "Cinema Exemplo",
            "cnpj": "12.345.678/0001-90",
            "telefone": "1234567890",
            "email": "cinema@gmail.com",
            "ativo": True,
            "endereco_id": create_address["id"]
        }
    
    def test_create_cinema_integration_success(self, client, cinema_data, create_address):
        response = client.post("/api/v1/cinema", json=cinema_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["nome"] == cinema_data["nome"]
        assert response_data["cnpj"] == cinema_data["cnpj"]
        assert response_data["endereco_id"] == create_address["id"]