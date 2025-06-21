from fastapi import status

class TestSalaControllerCreate:

    def test_create_sala_integration_success(self, client, sala_data):
        response = client.post("/api/v1/room", json=sala_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["nome"] == sala_data["nome"]
        assert response_data["capacidade"] == sala_data["capacidade"]
        assert response_data["cinema_id"] == sala_data["cinema_id"]