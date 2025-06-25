from sqlalchemy import Column, String, Integer, Boolean, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.assento_sala import AssentoSala
from app.models.base import BaseModel
from app.models.reserva import ItemReserva, Reserva

class Sessao(BaseModel):
    filme_id = Column(Integer, ForeignKey("filme.id"), nullable=False)
    sala_id = Column(Integer, ForeignKey("sala.id"), nullable=False)
    data = Column(Date, nullable=False)
    horario_ini = Column(DateTime, nullable=False)
    horario_fim = Column(DateTime, nullable=False)
    idioma = Column(String(50), nullable=False)
    legendado = Column(Boolean, default=False, nullable=False)
    formato = Column(String(20), nullable=False)  # 2D, 3D, IMAX, etc.
    preco_base = Column(Float, nullable=False)
    status = Column(String(20), default="ativa", nullable=False)  # ativa, cancelada, encerrada

    # Relacionamentos
    filme = relationship("Filme", back_populates="sessoes")
    sala = relationship("Sala", back_populates="sessoes")
    reservas = relationship("Reserva", back_populates="sessao", cascade="all, delete-orphan")

    def get_seats_available(self):
        from sqlalchemy.orm import object_session
        session = object_session(self)

        seat_room = session.query(AssentoSala).filter(
            AssentoSala.sala_id == self.sala_id,
            AssentoSala.ativo == "ativo"
        ).all()

        available_seats = [
            seat for seat in seat_room
            if not seat.is_session_reserved(self.id)
        ]

        return available_seats
    
    def get_seats_reserved(self):
        from sqlalchemy.orm import object_session
        session = object_session(self)

        seat_reserved = session.query(AssentoSala.codigo).join(
            ItemReserva, AssentoSala.id == ItemReserva.item_id
        ).join(Reserva).filter(
            ItemReserva.tipo == "assento",
            Reserva.sessao_id == self.id,
            Reserva.status.in_(["pendente", "confirmada"])
        )

        return [codigo[0] for codigo in seat_reserved]
    
    def calculate_seat_price(self, seat_room_id):
        from sqlalchemy.orm import object_session
        session = object_session(self)

        seat = session.query(AssentoSala).filter(
            AssentoSala.id == seat_room_id
        ).first()

        if not seat:
            return None
        
        return self.preco_base + seat.preco_adicional
    
    def get_ocupied(self):
        total_seats = len(self.sala.assentos)
        reserved_seats = len(self.get_seats_reserved())

        return {
            "total": total_seats,
            "reserved": reserved_seats,
            "available": total_seats - reserved_seats,
            "percentual_occupy": (reserved_seats / total_seats * 100) if total_seats > 0 else 0
        }

    def __repr__(self):
        return f"<Sessao(id={self.id}, filme_id={self.filme_id}, sala_id={self.sala_id}, data='{self.data}')>"