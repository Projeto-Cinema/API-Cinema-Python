import pytest

from fastapi import status

class TestEnderecoController:

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
    
    def test_create_address_integration(self, client, endereco_data):
        response = client.post("api/v1/address", json=endereco_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["cep"] == endereco_data["cep"]
        assert response_data["numero"] == endereco_data["numero"]
        assert response_data["bairro"] == endereco_data["bairro"]