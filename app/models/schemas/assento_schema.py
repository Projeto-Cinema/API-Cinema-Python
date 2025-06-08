from typing import Optional
from pydantic import BaseModel, Field

from app.models.schemas.enum.enum_util import StatusAssentoEnum

class AssentoBase(BaseModel):
    codigo: str
    tipo: str
    preco: float = Field(ge=0)
    status: StatusAssentoEnum = StatusAssentoEnum.DISPONIVEL

class AssentoCreate(AssentoBase):
    sessao_id: int

class AssentoUpdate(BaseModel):
    codigo: Optional[str] = None
    tipo: Optional[str] = None
    preco: Optional[float] = Field(None, ge=0)
    status: Optional[StatusAssentoEnum] = None

class AssentoResponse(AssentoBase):
    id: int
    sessao_id: int

    class Config:
        from_attributes = True

class AssentoListResponse(BaseModel):
    assentos: list[AssentoResponse] | None = None

    class Config:
        from_attributes = True