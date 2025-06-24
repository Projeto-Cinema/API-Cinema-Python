from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

PAYMENT_METHODS = Literal["cartao_credito", "cartao_debito", "pix", "boleto", "transferencia"]
PAYMENT_STATUS = Literal["pendente", "aprovado", "recusado", "reembolsado", "processado"]

class PagamentoBase(BaseModel):
    valor: float = Field(ge=0.0, description="Valor do pagamento, deve ser maior ou igual a zero")
    metodo: PAYMENT_METHODS = Field(description="Método de pagamento utilizado")
    status: PAYMENT_STATUS = Field(default="pendente", description="Status do pagamento")
    dt_pagamento: Optional[datetime] = Field(None, description="Data e hora do pagamento, se aplicável")
    referencia_externa: Optional[str] = Field(None, max_length=100, description="Referência do gateway de pagamento")

    @field_validator('valor')
    def validate_value(cls, v):
        if v <= 0:
            raise ValueError("Valor deve ser maior que zero")
        
        return round(v, 2)
    
    @field_validator('metodo')
    def validate_methods(cls, v):
        valid_methods = ["cartao_credito", "cartao_debito", "pix", "boleto", "transferencia"]
        if v not in valid_methods:
            raise ValueError(f"Método de pagamento inválido. Deve ser um dos: {', '.join(valid_methods)}")
        
        return v
    
    @field_validator('status')
    def validate_status(cls, v):
        valid_status = ["pendente", "aprovado", "recusado", "reembolsado", "processado"]
        if v not in valid_status:
            raise ValueError(f"Status inválido. Deve ser um dos: {', '.join(valid_status)}")
        
        return v

class PagamentoCreate(PagamentoBase):
    reserva_id: int = Field(gt=0, description="ID da reserva")

    @field_validator('reserva_id')
    def validate_reserva_id(cls, v):
        if v <= 0:
            raise ValueError("ID da reserva deve ser maior que zero")
        return v

class PagamentoUpdate(BaseModel):
    valor: Optional[float] = Field(None, gt=0.0, description="Valor do pagamento, deve ser maior que zero")
    metodo: Optional[PAYMENT_METHODS] = Field(None, description="Método de pagamento utilizado")
    status: Optional[PAYMENT_STATUS] = Field(None, description="Status do pagamento")
    dt_pagamento: Optional[datetime] = Field(None, description="Data e hora do pagamento, se aplicável")
    referencia_externa: Optional[str] = Field(None, max_length=100, description="Referência do gateway de pagamento")

    @field_validator('valor')
    def validate_value(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Valor deve ser maior que zero")
        return v

class PagamentoResponse(PagamentoBase):
    id: int
    reserva_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        form_attributes = True

class PagamentoWithReserve(PagamentoResponse):
    reserva: dict = Field(description="Detalhes da reserva associada ao pagamento")

class ComprovanteResponse(BaseModel):
    pagamento_id: int
    reserva_id: int
    codigo_reserva: int
    valor: float
    metodo: str
    dt_pagamento: datetime
    status: str
    referencia_externa: Optional[str] = None

    class Config:
        from_attributes = True

class StatusResponse(BaseModel):
    pagamento_id: int
    status: PAYMENT_STATUS
    dt_verificacao: datetime

    class Config:
        from_attributes = True