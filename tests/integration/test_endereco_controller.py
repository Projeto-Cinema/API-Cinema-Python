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

class TestEnderecoGetByID:

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
        assert response.status_code == status.HTTP_201_CREATEDs
        return response.json()
    
    def test_get_address_by_id_integration_success(self, client, create_address):
        address_id = create_address["id"]

        response = client.get(f"/api/v1/address/{address_id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == address_id
        assert response_data["cep"] == create_address["cep"]
        assert response_data["logradouro"] == create_address["logradouro"]