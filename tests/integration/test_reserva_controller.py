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

class TestReservaControllerGet:
    def test_get_reserva_by_id_integration_success(self, client, create_reserva):
        reserva_id = create_reserva["id"]

        response = client.get(f"/api/v1/reservas/{reserva_id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == reserva_id
        assert response_data["usuario_id"] == create_reserva["usuario_id"]
        assert response_data["sessao_id"] == create_reserva["sessao_id"]
        assert response_data["codigo"] == create_reserva["codigo"]
        assert response_data["status"] == create_reserva["status"]
        assert response_data["valor_total"] == create_reserva["valor_total"]

    def test_get_reserva_by_codigo_integration_success(self, client, create_reserva):
        codigo = create_reserva["codigo"]

        response = client.get(f"/api/v1/reservas/codigo/{codigo}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["codigo"] == codigo
        assert response_data["id"] == create_reserva["id"]

    def test_get_reservas_by_usuario_integration_success(self, client, create_reserva):
        usuario_id = create_reserva["usuario_id"]

        response = client.get(f"/api/v1/reservas/usuario/{usuario_id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) >= 1
        assert response_data[0]["usuario_id"] == usuario_id

class testReservaControllerUpdate:

    def test_update_reserva_integration_success(self, client, create_reserva, reserva_update_data):
        reserva_id = create_reserva["id"]

        response = client.put(f"/api/v1/reservas/{reserva_id}", json=reserva_update_data)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == reserva_id
        assert response_data["metodo_pagamento"] == reserva_update_data["metodo_pagamento"]
        if "valor_total" in reserva_update_data:
            assert response_data["valor_total"] == reserva_update_data["valor_total"]