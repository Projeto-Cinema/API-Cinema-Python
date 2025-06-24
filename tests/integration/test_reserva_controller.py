from fastapi import status

class TestReservaControllerCreate:

    def test_create_reserva_integration_success(self, client, reserva_data):
        response = client.post("/api/v1/reservas", json=reserva_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["usuario_id"] == reserva_data["usuario_id"]
        assert response_data["sessao_id"] == reserva_data["sessao_id"]
        assert response_data["status"] == reserva_data["status"]
        assert response_data["valor_total"] == reserva_data["valor_total"]
        assert response_data["assentos"] == reserva_data["assentos"]
        assert "codigo" in response_data
        assert len(response_data["codigo"]) == 8
        assert "id" in response_data
        assert "created_at" in response_data
        assert "updated_at" in response_data