from sqlalchemy import Column, String, Integer, Boolean, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Sessao(BaseModel):
    filme_id = Column(Integer, ForeignKey("filme.id"), nullable=False)
    sala_id = Column(Integer, ForeignKey("sala.id"), nullable=False)
    data = Column(Date, nullable=False)
    horario_ini = Column(DateTime, nullable=False)
    horario_fim = Column(DateTime, nullable=False)
    idioma = Column(String(50), nullable=False)
    legendado = Column(Boolean, default=False, nullable=False)
    formato = Column(String(20), nullable=False)  # 2D, 3D, IMAX, etc.
    preco_base = Column(Float, nullable=False)
    status = Column(String(20), default="ativa", nullable=False)  # ativa, cancelada, encerrada

    # Relacionamentos
    filme = relationship("Filme", back_populates="sessoes")
    sala = relationship("Sala", back_populates="sessoes")
    assentos = relationship("Assento", back_populates="sessao", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="sessao", cascade="all, delete-orphan")

class Assento(BaseModel):
    sessao_id = Column(Integer, ForeignKey("sessao.id"), nullable=False)
    codigo = Column(String(10), nullable=False)  # Ex: A1, B5, etc.
    tipo = Column(String(20), nullable=False)  # comum, vip, casal, etc.
    preco = Column(Float, nullable=False)
    status = Column(String(20), default="disponivel", nullable=False)  # disponivel, reservado, ocupado, indisponivel

    # Relacionamentos
    sessao = relationship("Sessao", back_populates="assentos")
    item_reserva = relationship("ItemReserva", back_populates="assento", uselist=False)