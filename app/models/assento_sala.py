from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class AssentoSala(BaseModel):
    sala_id = Column(Integer, ForeignKey("sala.id"), nullable=False)
    codigo = Column(String(10), nullable=False)
    tipo = Column(String(20), nullable=False)
    posicao_x = Column(Integer, nullable=True)
    posicao_y = Column(Integer, nullable=True)
    ativo = Column(String(20), default="ativo", nullable=False)

    # Relacionamento
    sala = relationship("Sala", back_populates="assentos")
    assentos_sessao = relationship("Assento", back_populates="assento_sala")

    def __repr__(self):
        return f"<AssentoSala(codigo='{self.codigo}', tipo='{self.tipo}', sala_id={self.sala_id})>"