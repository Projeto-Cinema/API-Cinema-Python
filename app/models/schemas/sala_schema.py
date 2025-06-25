from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.schemas.enum.enum_util import StatusSalaEnum

class AssentoSalaBase(BaseModel):
    codigo: str = Field(..., max_length=10)
    tipo: str = Field(..., max_length=20)
    posicao_x: Optional[int] = None
    posicao_y: Optional[int] = None
    preco_adicional: float = Field(default=0.0)
    ativo: str = Field(default="ativo", max_length=20)

class AssentoSalaCreate(AssentoSalaBase):
    pass

class AssentoSala(AssentoSalaBase):
    id: int

    class Config:
        orm_mode = True


class SalaBase(BaseModel):
    nome: str
    capacidade: int = Field(ge=0)
    tipo: str
    recursos: Optional[str] = None  # Lista de recursos em formato JSON
    mapa_assentos: Optional[str] = None  # Mapa de assentos em formato JSON
    status: StatusSalaEnum = StatusSalaEnum.ATIVA

class SalaCreate(SalaBase):
    cinema_id: int
    assentos: List[AssentoSalaCreate] = []

class SalaUpdate(BaseModel):
    cinema_id: Optional[int] = None
    nome: Optional[str] = None
    capacidade: Optional[int] = Field(None, ge=0)
    tipo: Optional[str] = None
    recursos: Optional[str] = None
    mapa_assentos: Optional[str] = None
    status: Optional[StatusSalaEnum] = None

class SalaResponse(SalaBase):
    id: int
    cinema_id: int
    assentos: List[AssentoSala] = []
    created_at: datetime

    class Config:
        form_attributes = True