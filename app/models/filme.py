from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Filme(BaseModel):
    titulo = Column(String(100), nullable=False)
    titulo_original = Column(String(100), nullable=False)
    sinopse = Column(Text, nullable=False)
    duracao_min = Column(Integer, nullable=False)
    diretor = Column(String(100), nullable=False)
    elenco = Column(Text, nullable=False)
    generos = Column(Text, nullable=False) # Lista de gêneros em formato JSON
    classificacao = Column(String(10), nullable=False)
    ano_lancamento = Column(Integer, nullable=False)
    em_cartaz = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    sessoes = relationship("Sessao", back_populates="filme", cascade="all, delete-orphan")