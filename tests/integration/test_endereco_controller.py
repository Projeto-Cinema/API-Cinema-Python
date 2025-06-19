from typing import Dict, List
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
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    
    def test_get_address_by_id_integration_success(self, client, create_address):
        address_id = create_address["id"]

        response = client.get(f"/api/v1/address/{address_id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == address_id
        assert response_data["cep"] == create_address["cep"]
        assert response_data["logradouro"] == create_address["logradouro"]

class TestEnderecoGetByCEP:

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
    
    def test_get_address_by_cep_integration_success(self, client, create_address):
        cep_data = create_address["cep"]

        response = client.get(f"/api/v1/address/cep/{cep_data}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == create_address["id"]
        assert response_data["cep"] == cep_data
        assert response_data["logradouro"] == create_address["logradouro"]

class TestEnderecoGetByAll:
    
    @pytest.fixture(scope="class")
    def enderecos_data(self):
        return [
            {
                "cep": "12345678",
                "logradouro": "Rua Exemplo",
                "numero": 123,
                "bairro": "Bairro Exemplo",
                "cidade": "Cidade Exemplo",
                "estado": "EX",
                "complemento": "Apto 1",
                "referencia": "ref exemplo",
            },
            {
                "cep": "222222",
                "logradouro": "Rua Exemplo",
                "numero": 222,
                "bairro": "Bairro Exemplo",
                "cidade": "Cidade Exemplo",
                "estado": "EX",
                "complemento": "Apto 1",
                "referencia": "ref exemplo",
            }
        ]
    
    @pytest.fixture
    def create_addresses(self, client, enderecos_data: List[Dict]):
        for address_data in enderecos_data:
            response = client.post("api/v1/address", json=address_data)
            assert response.status_code == status.HTTP_201_CREATED

    def test_list_all_addresses_without_filtering_integration(
        self,
        client,
        enderecos_data: List[Dict],
        create_addresses,
    ):
        response = client.get("api/v1/address")

        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == len(enderecos_data)
        
class TestEnderecoUpdate:

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
    
    def test_update_address_integration_success(self, client, create_address):
        address_id = create_address["id"]

        response = client.put(f"/api/v1/address/{address_id}", json={
            "logradouro": "Rua Atualizada",
            "numero": 456,
            "bairro": "Bairro Atualizado",
            "cidade": "Cidade Atualizada",
            "estado": "AT",
            "complemento": "Apto 2",
            "referencia": "ref atualizado"
        })

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == address_id
        assert response_data["logradouro"] == "Rua Atualizada"
        assert response_data["numero"] == 456

class TestEnderecoDelete:

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
    
    def test_delete_address_integration_success(self, client, create_address):
        address_id = create_address["id"]

        response = client.delete(f"/api/v1/address/{address_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = client.get(f"/api/v1/address/{address_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND