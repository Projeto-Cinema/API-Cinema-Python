from unittest.mock import Mock
from sqlalchemy.orm import Session

import pytest

from app.models.schemas.usuario_schema import UsuarioCreate
from app.models.usuario import Usuario
from app.service.usuario_service import UsuarioService


class TestUsuarioService:

    @pytest.fixture
    def usuario_service(self):
        return UsuarioService()
    
    @pytest.fixture
    def mock_db_session(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def usuario_create_data(self):
        return UsuarioCreate(
            nome="Wesley",
            email="weslin@gmail.com",
            cpf="12345678901",
            senha="senha123",
        )
    
    @pytest.fixture
    def usuario_model_mock(self):
        usuario_mock = Mock(spec=Usuario)
        usuario_mock.id = 1
        usuario_mock.nome = "Wesley"
        usuario_mock.email = "weslin@gmail.com"
        usuario_mock.cpf = "12345678901"
        usuario_mock.senha = "hashed_senha123"
        return usuario_mock
    
class TestUsuarioServiceInit:
    
    def test_init_creates_pwd_context(self):
        service = UsuarioService()

        assert service.pwd_context is not None
        assert "bcrypt" in service.pwd_context.schemes()