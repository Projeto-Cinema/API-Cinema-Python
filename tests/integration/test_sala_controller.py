from typing import Dict, List
from fastapi import status

from app.models.schemas.enum.enum_util import StatusSalaEnum

class TestSalaControllerCreate:

    def test_create_sala_integration_success(self, client, sala_data):
        response = client.post("/api/v1/room", json=sala_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["nome"] == sala_data["nome"]
        assert response_data["capacidade"] == sala_data["capacidade"]
        assert response_data["cinema_id"] == sala_data["cinema_id"]

class TestSalaControllerGet:

    def test_get_sala_by_id_integration_success(self, client, create_sala):
        sala_id = create_sala["id"]

        response = client.get(f"/api/v1/room/{sala_id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == sala_id
        assert response_data["nome"] == create_sala["nome"]
        assert response_data["capacidade"] == create_sala["capacidade"]
        assert response_data["cinema_id"] == create_sala["cinema_id"]

    def test_get_sala_by_id_not_found(self, client):
        response = client.get("/api/v1/room/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_all_salas_integration_success(self, client, salas_data: List[Dict], create_rooms):
        response = client.get("/api/v1/room")

        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == len(salas_data)

class TestSalaControllerUpdate:

    def test_update_sala_integration_success(self, client, create_sala):
        sala_id = create_sala["id"]
        updated_data = {
            "nome": "Sala Atualizada",
            "capacidade": 120,
            "tipo": "IMAX",
            "recursos": '{"projetor": "4K", "som": "Dolby Atmos"}',
            "mapa_assentos": '{"A": [1, 2, 3], "B": [1, 2, 3]}',
            "status": StatusSalaEnum.ATIVA
        }

        response = client.put(f"/api/v1/room/{sala_id}", json=updated_data)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["nome"] == updated_data["nome"]
        assert response_data["capacidade"] == updated_data["capacidade"]

    def test_update_sala_not_found(self, client):
        updated_data = {
            "nome": "Sala Inexistente",
            "capacidade": 100,
            "tipo": "IMAX",
            "recursos": '{"projetor": "4K", "som": "Dolby Atmos"}',
            "mapa_assentos": '{"A": [1, 2, 3], "B": [1, 2, 3]}',
            "status": StatusSalaEnum.ATIVA
        }

        response = client.put("/api/v1/room/9999", json=updated_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

class TestSalaControllerDelete:

    def test_parcial_delete_sala_integration_success(self, client, create_sala):
        sala_id = create_sala["id"]

        response = client.delete(f"/api/v1/room/{sala_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = client.get(f"/api/v1/room/{sala_id}")
        response_data = response.json()
        assert response_data["status"] == StatusSalaEnum.INATIVO

    def test_delete_sala_integration_success(self, client, create_sala):
        sala_id = create_sala["id"]

        response = client.delete(f"/api/v1/room/delete/{sala_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = client.get(f"/api/v1/room/{sala_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND