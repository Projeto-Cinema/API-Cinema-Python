from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Cinema(BaseModel):
    endereco_id = Column(Integer, ForeignKey("endereco.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    site = Column(String(255), nullable=True)
    horario_func = Column(String(50), nullable=True)
    imagem_url = Column(String(255), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    endereco = relationship("Endereco", back_populates="cinema")
    salas = relationship("Sala", back_populates="cinema", cascade="all, delete-orphan")
    produtos = relationship("Produto", back_populates="cinema", cascade="all, delete-orphan")

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