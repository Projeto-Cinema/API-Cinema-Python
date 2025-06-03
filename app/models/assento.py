from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Assento(BaseModel):
    sessao_id = Column(Integer, ForeignKey("sessao.id"), nullable=False)
    codigo = Column(String(10), nullable=False)  # Ex: A1, B5, etc.
    tipo = Column(String(20), nullable=False)  # comum, vip, casal, etc.
    preco = Column(Float, nullable=False)
    status = Column(String(20), default="disponivel", nullable=False)  # disponivel, reservado, ocupado, indisponivel

    # Relacionamentos
    sessao = relationship("Sessao", back_populates="assentos")
    item_reserva = relationship("ItemReserva", back_populates="assento", uselist=False)