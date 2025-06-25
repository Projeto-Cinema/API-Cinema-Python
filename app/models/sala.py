from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Sala(BaseModel):
    cinema_id = Column(Integer, ForeignKey("cinema.id"), nullable=False)
    nome = Column(String(50), nullable=False)
    capacidade = Column(Integer, nullable=False)
    tipo = Column(String(20), nullable=False)
    recursos = Column(String(255), nullable=True) # Vai armazenar a lista em formato JSON
    mapa_assentos = Column(Text, nullable=True) # Vai armazenar o mapa de assentos em formato JSON
    status = Column(String(20), nullable=False, default="ativo") # ativo, em_manutencao, inativo

    # Relacionamentos
    cinema = relationship("Cinema", back_populates="salas")
    sessoes = relationship("Sessao", back_populates="sala", cascade="all, delete-orphan")
    assentos = relationship("AssentoSala", back_populates="sala", cascade="all, delete-orphan")