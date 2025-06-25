from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.reserva import ItemReserva, Reserva


class AssentoSala(BaseModel):
    __tablename__ = "assento_sala"
    sala_id = Column(Integer, ForeignKey("sala.id"), nullable=False)
    codigo = Column(String(10), nullable=False)
    tipo = Column(String(20), nullable=False)
    posicao_x = Column(Integer, nullable=True)
    posicao_y = Column(Integer, nullable=True)
    preco_adicional = Column(Float, default=0.0, nullable=False)
    ativo = Column(String(20), default="ativo", nullable=False)

    # Relacionamento
    sala = relationship("Sala", back_populates="assentos")

    def is_session_reserved(self, sessao_id: int):
        from sqlalchemy.orm import object_session
        session = object_session(self)

        active_session = session.query(ItemReserva).join(Reserva).filter(
            ItemReserva.tipo == "assento",
            ItemReserva.item_id == self.id,
            Reserva.sessao_id == sessao_id,
            Reserva.status.in_(["pendente", "confirmada"])
        ).first()

        return active_session is not None

    def __repr__(self):
        return f"<AssentoSala(codigo='{self.codigo}', tipo='{self.tipo}', sala_id={self.sala_id})>"