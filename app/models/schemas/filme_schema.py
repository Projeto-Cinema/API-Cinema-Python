from typing import Optional
from pydantic import BaseModel, Field


class FilmeBase(BaseModel):
    titulo: str
    titulo_original: str
    sinopse: str
    duracao_min: int = Field(ge=1)
    diretor: str
    elenco: str
    generos: list[str]
    classificacao: str
    ano_lancamento: int = Field(ge=1)
    em_cartaz: bool = True

class FilmeCreate(FilmeBase):
    pass

class FilmeUpdate(BaseModel):
    titulo: Optional[str] = None
    titulo_original: Optional[str] = None
    sinopse: Optional[str] = None
    duracao_min: Optional[int] = Field(None, ge=1)
    diretor: Optional[str] = None
    elenco: Optional[str] = None
    generos: Optional[str] = None
    classificacao: Optional[str] = None
    ano_lancamento: Optional[int] = Field(None, ge=1)
    em_cartaz: Optional[bool] = None

class FilmeResponse(FilmeBase):
    id: int

    class Config:
        from_attributes = True
        json_encoders = {
            list: lambda v: ', '.join(v)  # Converte listas para strings
        }