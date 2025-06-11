
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Reserva(BaseModel):
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    sessao_id = Column(Integer, ForeignKey("sessao.id"), nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    data_reserva = Column(DateTime, nullable=False)
    status = Column(String(20), default="pendente", nullable=False)  # pendente, confirmada, cancelada, expirada
    valor_total = Column(Float, nullable=False)
    metodo_pagamento = Column(String(50), nullable=True)
    assentos = Column(Text, nullable=False)  # Armazenará uma lista de códigos em formato JSON

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="reservas")
    sessao = relationship("Sessao", back_populates="reservas")
    itens = relationship("ItemReserva", back_populates="reserva", cascade="all, delete-orphan")
    pagamento = relationship("Pagamento", back_populates="reserva", uselist=False)

class ItemReserva(BaseModel):
    reserva_id = Column(Integer, ForeignKey("reserva.id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    tipo = Column(String(20), nullable=False)  # assento ou produto
    quantidade = Column(Integer, default=1, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    preco_total = Column(Float, nullable=False)
    desconto = Column(Float, default=0, nullable=False)

    # Relacionamentos
    reserva = relationship("Reserva", back_populates="itens")
    produto = relationship(
        "Produto", 
        foreign_keys=[item_id], 
        primaryjoin="and_(ItemReserva.tipo == 'produto', ItemReserva.item_id==Produto.id)", 
        viewonly=True
    )
    assento = relationship(
        "Assento", 
        foreign_keys=[item_id], 
        primaryjoin="and_(ItemReserva.tipo=='assento', ItemReserva.item_id==Assento.id)", 
        viewonly=True
    )