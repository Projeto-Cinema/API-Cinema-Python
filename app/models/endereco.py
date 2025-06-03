from datetime import datetime
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Endereco(BaseModel):
    cep = Column(String(10), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    referencia = Column(String(255), nullable=True)

    # Relacionamentos
    cinema = relationship("Cinema", back_populates="endereco", uselist=False)