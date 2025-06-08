from typing import Optional
from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    categoria: str
    preco: float = Field(ge=0)
    imagem_url: str
    disponivel: bool = True

class ProdutoCreate(ProdutoBase):
    cinema_id: int

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    preco: Optional[float] = Field(None, ge=0)
    imagem_url: Optional[str] = None
    disponivel: Optional[bool] = None

class ProdutoResponse(ProdutoBase):
    id: int
    cinema_id: int

    class Config:
        from_attributes = True
        json_encoders = {
            list: lambda v: ', '.join(v)
        }

class ProdutoListResponse(ProdutoResponse):
    class Config:
        from_attributes = True
        json_encoders = {
            list: lambda v: ', '.join(v)
        }