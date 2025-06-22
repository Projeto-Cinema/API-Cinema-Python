from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Assento(BaseModel):
    sessao_id = Column(Integer, ForeignKey("sessao.id"), nullable=False)
    assento_sala_id = Column(Integer, ForeignKey("assento_sala.id"), nullable=False)
    preco = Column(Float, nullable=False)
    status = Column(String(20), default="disponivel", nullable=False)  # disponivel, reservado, ocupado, indisponivel

    # Relacionamentos
    sessao = relationship("Sessao", back_populates="assentos")
    assento_sala = relationship("AssentoSala", back_populates="assentos_sessao")

    @property
    def codigo(self):
        return self.assento_sala.codigo if self.assento_sala else None
    
    @property
    def tipo(self):
        return self.assento_sala.tipo if self.assento_sala else None
    
    @property
    def posicao_x(self):
        return self.assento_sala.posicao_x if self.assento_sala else None
    
    @property
    def posicao_y(self):
        return self.assento_sala.posicao_y if self.assento_sala else None

    def __repr__(self):
        return f"<Assento(codigo='{self.codigo}', status='{self.status}', sessao_id={self.sessao_id})>"