from ast import List
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.schemas.enum.enum_util import StatusReservaEnum
from app.models.schemas.item_reserva_schema import ItemReservaCreate


class ReservaBase(BaseModel):
    codigo: str = Field(max_length=20)
    data_reserva: datetime
    status: StatusReservaEnum = StatusReservaEnum.PENDENTE
    valor_total: float = Field(ge=0)
    metodo_pagamento: Optional[str] = Field(None, max_length=50)
    assentos: str

class ReservaCreate(ReservaBase):
    usuario_id: int
    sessao_id: int
    itens: List[ItemReservaCreate] = []

class ReservaUpdate(BaseModel):
    status: Optional[StatusReservaEnum] = None
    valor_total: Optional[float] = Field(None, ge=0)
    metodo_pagamento: Optional[str] = Field(None, max_length=50)
    assentos: Optional[str] = None

class ReservaResponse(ReservaBase):
    id: int
    usuario_id: int
    sessao_id: int
    created_at: datetime
    updated_at: datetime
    itens: List[ItemReservaCreate] = []

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }