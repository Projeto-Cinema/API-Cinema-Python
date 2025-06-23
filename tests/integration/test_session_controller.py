from fastapi import status

class TestSessaoControllerCreate:
    def test_create_session(self, client, session_data):
        response = client.post("/session", json=session_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["filme_id"] == session_data["filme_id"]
        assert data["sala_id"] == session_data["sala_id"]
        assert data["idioma"] == session_data["idioma"]