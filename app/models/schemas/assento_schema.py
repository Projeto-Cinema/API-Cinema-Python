from typing import Optional
from pydantic import BaseModel, Field

from app.models.schemas.enum.enum_util import StatusAssentoEnum

class AssentoBase(BaseModel):
    preco: float = Field(ge=0)
    status: StatusAssentoEnum = StatusAssentoEnum.DISPONIVEL

class AssentoCreate(AssentoBase):
    sessao_id: int
    assento_sala_id: int

class AssentoUpdate(BaseModel):
    preco: Optional[float] = Field(None, ge=0)
    status: Optional[StatusAssentoEnum] = None

class AssentoResponse(AssentoBase):
    id: int
    sessao_id: int
    assento_sala_id: int
    # Dados derivados do assento físico
    codigo: Optional[str] = None
    tipo: Optional[str] = None
    posicao_x: Optional[int] = None
    posicao_y: Optional[int] = None

    class Config:
        from_attributes = True

class AssentoListResponse(BaseModel):
    assentos: list[AssentoResponse]

    class Config:
        from_attributes = True

# Schema específico para exibir assentos na sessão (mais limpo para frontend)
class AssentoSessaoView(BaseModel):
    id: int
    codigo: str
    tipo: str
    preco: float
    status: StatusAssentoEnum
    posicao_x: Optional[int] = None
    posicao_y: Optional[int] = None

    class Config:
        from_attributes = True