from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.filme import filme_genero


class Genero(BaseModel):
    nome = Column(String(50), nullable=False, unique=True)

    # Relacionamentos
    filmes = relationship("Filme", secondary=filme_genero, back_populates="generos")