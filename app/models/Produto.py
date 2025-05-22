from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Produto(BaseModel):
    cinema_id = Column(Integer, ForeignKey("cinema.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    categoria = Column(String(50), nullable=False)  # bebida, comida, combo, etc.
    preco = Column(Float, nullable=False)
    imagem_url = Column(String(255), nullable=True)
    disponivel = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    cinema = relationship("Cinema", back_populates="produtos")

class Pagamento(BaseModel):
    reserva_id = Column(Integer, ForeignKey("reserva.id"), nullable=False, unique=True)
    valor = Column(Float, nullable=False)
    metodo = Column(String(50), nullable=False)  # cartão de crédito, débito, pix, etc.
    status = Column(String(20), default="pendente", nullable=False)  # pendente, aprovado, recusado, reembolsado
    dt_pagamento = Column(DateTime, nullable=True)
    referencia_externa = Column(String(100), nullable=True)  # Referência do gateway de pagamento

    # Relacionamentos
    reserva = relationship("Reserva", back_populates="pagamento")