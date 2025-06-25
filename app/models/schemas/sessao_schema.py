from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field

from app.models.schemas.enum.enum_util import StatusSessaoEnum

class SessaoBase(BaseModel):
    data: date
    horario_ini: datetime
    horario_fim: datetime
    idioma: str
    legendado: bool
    formato: str
    preco_base: float = Field(ge=0)
    status: StatusSessaoEnum = StatusSessaoEnum.ATIVA

class SessaoCreate(SessaoBase):
    filme_id: int
    sala_id: int

class SessaoUpdate(BaseModel):
    data: Optional[date] = None
    horario_ini: Optional[datetime] = None
    horario_fim: Optional[datetime] = None
    idioma: Optional[str] = None
    legendado: Optional[bool] = None
    formato: Optional[str] = None
    preco_base: Optional[float] = Field(None, ge=0)
    status: Optional[StatusSessaoEnum] = None

class SessaoResponse(SessaoBase):
    id: int
    filme_id: int
    sala_id: int

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            date: lambda v: v.isoformat() if v else None
        }

class SessaoListResponse(SessaoResponse):
    sessao: list[SessaoResponse]
    total: int