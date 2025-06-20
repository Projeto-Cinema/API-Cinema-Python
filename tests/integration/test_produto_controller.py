from fastapi import status

class TestProdutoController:

    def test_create_product_integration_success(self, client, product_payload):
        response = client.post("/api/v1/products", json=product_payload)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["nome"] == product_payload["nome"]
        assert response_data["preco"] == product_payload["preco"]