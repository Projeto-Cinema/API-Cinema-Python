from typing import Optional
from pydantic import BaseModel

class AssentoSalaBase(BaseModel):
    codigo: str
    tipo: str
    posicao_x: Optional[int] = None
    posicao_y: Optional[int] = None
    ativo: str = "ativo"

class AssentoSalaCreate(AssentoSalaBase):
    sala_id: int

class AssentoSalaUpdate(BaseModel):
    codigo: Optional[str] = None
    tipo: Optional[str] = None
    posicao_x: Optional[int] = None
    posicao_y: Optional[int] = None
    ativo: Optional[str] = None

class AssentoSalaResponse(AssentoSalaBase):
    id: int
    sala_id: int

    class Config:
        from_attributes = True

class AssentoSalaListResponse(BaseModel):
    assentos: list[AssentoSalaResponse]
    
    class Config:
        from_attributes = True