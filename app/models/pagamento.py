from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Pagamento(BaseModel):
    reserva_id = Column(Integer, ForeignKey("reserva.id"), nullable=False, unique=True)
    valor = Column(Float, nullable=False)
    metodo = Column(String(50), nullable=False)  # cartão de crédito, débito, pix, etc.
    status = Column(String(20), default="pendente", nullable=False)  # pendente, aprovado, recusado, reembolsado
    dt_pagamento = Column(DateTime, nullable=True)
    referencia_externa = Column(String(100), nullable=True)  # Referência do gateway de pagamento

    # Relacionamentos
    reserva = relationship("Reserva", back_populates="pagamento")