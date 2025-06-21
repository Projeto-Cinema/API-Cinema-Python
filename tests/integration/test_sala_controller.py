from typing import Dict, List
from fastapi import status

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