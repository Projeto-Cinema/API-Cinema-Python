from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.schemas.enum.enum_util import StatusSalaEnum


class SalaBase(BaseModel):
    nome: str
    capacidade: int = Field(ge=0)
    tipo: str
    recursos: Optional[str] = None  # Lista de recursos em formato JSON
    mapa_assentos: Optional[str] = None  # Mapa de assentos em formato JSON
    status: StatusSalaEnum = StatusSalaEnum.ATIVA

class SalaCreate(SalaBase):
    cinema_id: int

class SalaUpdate(BaseModel):
    nome: Optional[str] = None
    capacidade: Optional[int] = Field(None, ge=0)
    tipo: Optional[str] = None
    recursos: Optional[str] = None
    mapa_assentos: Optional[str] = None
    status: Optional[StatusSalaEnum] = None

class SalaResponse(SalaBase):
    id: int
    cinema_id: int
    created_at: datetime

    class Config:
        form_attributes = True
