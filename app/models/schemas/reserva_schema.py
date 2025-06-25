from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.schemas.enum.enum_util import StatusReservaEnum
from app.models.schemas.item_reserva_schema import ItemReservaCreate, ItemReservaResponse


class ReservaBase(BaseModel):
    codigo: str = Field(max_length=20)
    data_reserva: datetime
    status: StatusReservaEnum = StatusReservaEnum.PENDENTE
    valor_total: float = Field(ge=0)
    metodo_pagamento: Optional[str] = Field(None, max_length=50)

class ReservaCreate(ReservaBase):
    usuario_id: int
    sessao_id: int
    itens: List[ItemReservaCreate] = []

class ReservaUpdate(BaseModel):
    data_reserva: Optional[datetime] = None
    status: Optional[StatusReservaEnum] = None
    valor_total: Optional[float] = Field(None, ge=0)
    metodo_pagamento: Optional[str] = Field(None, max_length=50)

class ReservaResponse(ReservaBase):
    id: int
    usuario_id: int
    sessao_id: int
    created_at: datetime
    updated_at: datetime
    itens: List[ItemReservaResponse] = []

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }