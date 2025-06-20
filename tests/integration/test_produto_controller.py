from fastapi import status

class TestProdutoController:

    def test_create_product_integration_success(self, client, product_payload):
        response = client.post("/api/v1/products", json=product_payload)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["nome"] == product_payload["nome"]
        assert response_data["preco"] == product_payload["preco"]

class TestProdutoControllerGetProduct:

    def test_get_product_by_id_integration_success(self, client, create_product):
        product_id = create_product["id"]

        response = client.get(f"/api/v1/products/{product_id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == product_id
        assert response_data["nome"] == create_product["nome"]
        assert response_data["preco"] == create_product["preco"]

    def test_get_product_by_id_not_found(self, client):
        response = client.get("/api/v1/products/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_product_by_name_integration_success(self, client, create_product):
        product_name = create_product["nome"]

        response = client.get(f"/api/v1/products/name/{product_name}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["nome"] == product_name
        assert response_data["preco"] == create_product["preco"]

    def test_get_all_products_integration_success(self, client, create_products):
        response = client.get("/api/v1/products")

        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == len(create_products)

class TestProdutoControllerUpdate:

    def test_update_product_integration_success(self, client, create_product):
        product_id = create_product["id"]
        update_payload = {
            "nome": "Produto Atualizado",
            "descricao": "Descrição atualizada",
            "categoria": "Bebidas",
            "preco": 29.99,
            "imagem_url": "http://example.com/imagem_atualizada.jpg",
            "disponivel": False
        }

        response = client.put(f"/api/v1/products/{product_id}", json=update_payload)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["nome"] == update_payload["nome"]
        assert response_data["preco"] == update_payload["preco"]
        assert response_data["disponivel"] == update_payload["disponivel"]

class TestProdutoControllerDelete:

    def test_parcial_delete_product_integration_success(self, client, create_product):
        product_id = create_product["id"]

        response = client.delete(f"/api/v1/products/{product_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica se o produto foi desativado
        response_check = client.get(f"/api/v1/products/{product_id}")
        response_data = response_check.json()
        assert response_data["disponivel"] is False