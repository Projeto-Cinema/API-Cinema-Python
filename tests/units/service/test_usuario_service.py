from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

import pytest

from app.models.schemas.usuario_schema import UsuarioCreate
from app.models.usuario import Usuario
from app.service.usuario_service import UsuarioService, usuario_service


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
            ativo=True
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

class TestUsuarioServicePasswordMethods:

    def test_hash_password(self):
        password = "senha123"

        hashed = usuario_service._hash_password(password)

        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password(self):
        password = "senha123"
        hashed = usuario_service._hash_password(password)

        result = usuario_service._verify_password(password, hashed)

        assert result is True

class TestUsuarioServiceCreateUser:

    @patch('app.models.usuario.Usuario')
    def test_create_user_success(
        self, 
        mock_usuario_class,
        mock_db_session, 
        usuario_create_data, 
        usuario_model_mock
    ):
        # Arrange
        mock_usuario_class.return_value = usuario_model_mock
        mock_db_session.add = Mock()
        mock_db_session.commit = Mock()
        mock_db_session.refresh = Mock()

        # Act
        result = usuario_service.create_user(mock_db_session, usuario_create_data)

        # Assert
        assert result == usuario_model_mock
        mock_db_session.add.assert_called_once_with(usuario_model_mock)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(usuario_model_mock)

        # Verificar argumentos passados para Usuario()
        call_args = mock_usuario_class.call_args[1]  # kwargs do construtor
        assert call_args['senha'] != usuario_create_data.senha  # Senha deve estar hasheada
        assert call_args['nome'] == usuario_create_data.nome
        assert call_args['email'] == usuario_create_data.email
        assert call_args['cpf'] == usuario_create_data.cpf
