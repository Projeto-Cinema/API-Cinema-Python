"""Configuração do FastAPI com Pydantic e Pydantic Settings."""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações do FastAPI usando Pydantic Settings.

    Esta classe define as configurações do projeto, incluindo nome, versão,
    descrição, URL do banco de dados, chave secreta, algoritmo de autenticação,
    tempo de expiração do token de acesso e origens CORS permitidas.
    """

    PROJECT_NAME: str = "Cinema API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "API para gerenciamento de cinema"

    DATABASE_URL: str = "postgresql://fastapi_db_cenc_user:FmYrITLWvd3CYku92acH6zUut13IwRPi@dpg-d1tf4smr433s73dmb0lg-a/fastapi_db_cenc"
    #DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/fastapi_db"

    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CORS_ORIGINS: list[str] = ["*"]

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
