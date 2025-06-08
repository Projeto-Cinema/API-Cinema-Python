from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.schemas.enum.enum_util import TipoItemEnum


class ItemReservaBase(BaseModel):
    item_id: int
    tipo: TipoItemEnum
    quantidade: int = Field(ge=1, default=1)
    preco_unitario: float = Field(ge=0)
    preco_total: float = Field(ge=0)
    desconto: float = Field(ge=0, default=0)

class ItemReservaCreate(ItemReservaBase):
    pass

class ItemReservaUpdate(BaseModel):
    quantidade: Optional[int] = Field(ge=1, default=1)
    preco_unitario: Optional[float] = Field(ge=0)
    preco_total: Optional[float] = Field(ge=0)
    desconto: Optional[float] = Field(ge=0, default=0)

class ItemReservaResponse(ItemReservaBase):
    id: int
    reserva_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }