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

class TestFilmeControllerGet:

    def test_get_movie_by_id_integration_success(self, client, create_movie):
        movie_id = create_movie["id"]

        response = client.get(f"/api/v1/movies/{movie_id}")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == movie_id
        assert response_data["titulo"] == create_movie["titulo"]