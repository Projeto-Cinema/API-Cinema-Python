from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.schemas.genero_schema import Genero

class FilmeBase(BaseModel):
    titulo: str
    titulo_original: str
    sinopse: str
    duracao_min: int = Field(ge=1)
    diretor: str
    elenco: str
    classificacao: str
    ano_lancamento: int = Field(ge=1900)
    em_cartaz: bool = True

class FilmeCreate(FilmeBase):
    generos_id: List[int] = Field(..., description="Lista de IDs dos gêneros associados ao filme")

class FilmeUpdate(BaseModel):
    titulo: Optional[str] = None
    titulo_original: Optional[str] = None
    sinopse: Optional[str] = None
    duracao_min: Optional[int] = Field(None, ge=1)
    diretor: Optional[str] = None
    elenco: Optional[str] = None
    classificacao: Optional[str] = None
    ano_lancamento: Optional[int] = Field(None, ge=1900)
    em_cartaz: Optional[bool] = None

class FilmeResponse(FilmeBase):
    id: int
    generos: List[Genero] = Field(..., description="Lista de nomes dos gêneros associados ao filme")

    class Config:
        from_attributes = True
        json_encoders = {
            list: lambda v: ', '.join(v)  # Converte listas para strings
        }