from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Usuario(BaseModel):
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)
    dt_nascimento = Column(DateTime, nullable=True)
    cpf = Column(String(14), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    dt_cadastro = Column(DateTime, default=datetime.utcnow, nullable=False)
    tipo = Column(String(20), nullable=False, default="cliente")
    ultimo_acesso = Column(DateTime, nullable=True)

    # Relacionamentos
    reservas = relationship("Reserva", back_populates="usuario", cascade="all, delete-orphan")