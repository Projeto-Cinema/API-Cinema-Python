from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

# Tabela de associação
filme_genero = Table(
    'filme_genero',
    BaseModel.metadata,
    Column('filme_id', Integer, ForeignKey('filme.id'), primary_key=True),
    Column('genero_id', Integer, ForeignKey('genero.id'), primary_key=True)
)

class Filme(BaseModel):
    titulo = Column(String(100), nullable=False)
    titulo_original = Column(String(100), nullable=False)
    sinopse = Column(Text, nullable=False)
    duracao_min = Column(Integer, nullable=False)
    diretor = Column(String(100), nullable=False)
    elenco = Column(Text, nullable=False)
    classificacao = Column(String(10), nullable=False)
    ano_lancamento = Column(Integer, nullable=False)
    em_cartaz = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    sessoes = relationship("Sessao", back_populates="filme", cascade="all, delete-orphan")
    generos = relationship("Genero", secondary=filme_genero, back_populates="filmes")