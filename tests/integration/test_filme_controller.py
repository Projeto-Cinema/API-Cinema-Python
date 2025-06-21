from fastapi import status

class TestFilmeControllerCreate:

    def test_create_filme_integration_success(self, client, filme_data):
        response = client.post("/api/v1/movies", json=filme_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["titulo"] == filme_data["titulo"]
        assert response_data["duracao_min"] == filme_data["duracao_min"]
        assert response_data["classificacao"] == filme_data["classificacao"]
        
        assert len(response_data["generos"]) == len(filme_data["generos_id"])
        generos_ids_response = [genero["id"] for genero in response_data["generos"]]
        assert set(generos_ids_response) == set(filme_data["generos_id"])