from itertools import count
from typing import List
from passlib.context import CryptContext

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from app.models import sessao
from app.models.assento import Assento
from app.models.schemas.assento_schema import AssentoCreate, AssentoResponse, AssentoSessaoView, AssentoUpdate
from app.models.schemas.enum.enum_util import StatusAssentoEnum
from app.models.sessao import Sessao
from app.models.assento_sala import AssentoSala

class AssentoService:

    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_seat_to_session(self, db: Session, session_id: int, room_id: int, base_price: float) -> List[AssentoResponse]:
        db_session = db.query(Sessao).filter(Sessao.id == session_id).first()
        if not db_session:
            raise ValueError("Sessão não encontrada")
        
        existing_seats = db.query(Assento).filter(Assento.sessao_id == session_id).first()
        if existing_seats:
            raise ValueError("Sessão já possui assentos cadastrados")
        
        seats_room = db.query(AssentoSala).filter(
            and_(
                AssentoSala.sala_id == room_id,
                AssentoSala.ativo == "ativo"
            )
        ).all()

        if not seats_room:
            raise ValueError("Nenhum assento disponível na sala")
        
        new_seats = []
        for seat in seats_room:
            final_price = self._calculate_type_price(seat.tipo, base_price)

            session_seat = Assento(
                sessao_id=session_id,
                assento_sala_id=seat.id,
                preco=final_price,
                status=StatusAssentoEnum.DISPONIVEL.value
            )

            db.add(session_seat)
            new_seats.append(session_seat)

        db.commit()

        for seat in new_seats:
            db.refresh(seat)

        return [self._to_response(seat) for seat in new_seats]
    
    def create_seat(self, db: Session, seat_data: AssentoCreate) -> AssentoResponse:
        session = db.query(Sessao).filter(Sessao.id == seat_data.sessao_id).first()
        if not session:
            raise ValueError("Sessão não encontrada")
        
        seat_room = db.query(AssentoSala).filter(AssentoSala.id == seat_data.assento_sala_id).first()
        if not seat_room:
            raise ValueError("Assento de sala não encontrado")
        
        existing_seat = db.query(Assento).filter(
            and_(
                Assento.sessao_id == seat_data.sessao_id,
                Assento.assento_sala_id == seat_data.assento_sala_id
            )
        ).first()

        if not existing_seat:
            raise ValueError("Assento já cadastrado na sessão")
        
        seat = Assento(**seat_data.dict())
        db.add(seat)
        db.commit()
        db.refresh(seat)

        return self._to_response(seat)
    
    def search_seat_by_id(self, db: Session, seat_id: int) -> AssentoResponse:
        seat = db.query(Assento).options(
            joinedload(Assento.assento_sala)
        ).filter(Assento.id == seat_id).first()

        if not seat:
            raise ValueError("Assento não encontrado")
        
        return self._to_response(seat)
    
    def search_seats_by_session(self, db: Session, session_id: int, only_available: bool = False) -> List[AssentoSessaoView]:
        query = db.query(Assento).options(
            joinedload(Assento.assento_sala)
        ).filter(Assento.sessao_id == session_id)

        if only_available:
            query = query.filter(Assento.status == StatusAssentoEnum.DISPONIVEL.value)

        seats = query.order_by(Assento.assento_sala.has(AssentoSala.codigo)).all()

        return [self._to_sessao_view(seat) for seat in seats]
    
    def update_seat(self, db: Session, seat_id: int, seat_data: AssentoUpdate) -> AssentoResponse:
        seat = db.query(Assento).filter(Assento.id == seat_id).first()
        if not seat:
            raise ValueError("Assento não encontrado")
        
        update_data = seat_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(seat, key, value)

        db.commit()
        db.refresh(seat)

        return self._to_response(seat)
    
    def delete_seat(self, db: Session, seat_id: int) -> bool:
        seat = db.query(Assento).filter(Assento.id == seat_id).first()
        if not seat:
            raise ValueError("Assento não encontrado")
        
        if seat.status in [StatusAssentoEnum.RESERVADO.value, StatusAssentoEnum.OCUPADO.value]:
            raise ValueError("Assento não pode ser excluído, pois está reservado ou ocupado")
        
        db.delete(seat)
        db.commit()

        return True
    
    def delete_seats_from_session(self, db: Session, session_id: int) -> bool:
        seats = db.query(Assento).filter(Assento.sessao_id == session_id).all()

        for seat in seats:
            db.delete(seat)

        db.commit()
        return True
    
    # =================== Métodos Privados =================== #

    def reserve_seat(self, seat_id: int) -> AssentoResponse:
        return self._update_seat_status(seat_id, StatusAssentoEnum.RESERVADO)
    
    def occupy_seat(self, seat_id: int) -> AssentoResponse:
        return self._update_seat_status(seat_id, StatusAssentoEnum.OCUPADO)
    
    def liberate_seat(self, seat_id: int) -> AssentoResponse:
        return self._update_seat_status(seat_id, StatusAssentoEnum.DISPONIVEL)
    
    def unliberate_seat(self, seat_id: int) -> AssentoResponse:
        return self._update_seat_status(seat_id, StatusAssentoEnum.INDISPONIVEL)
    
    def reserve_many_seats(self, db: Session, seat_ids: List[int]) -> List[AssentoResponse]:
        updated_seats = []

        seats = db.query(Assento).filter(Assento.id.in_(seat_ids)).all()

        if len(seats) != len(seat_ids):
            raise ValueError("Alguns assentos não foram encontrados")
    
        for seat in seats:
            if seat.status != StatusAssentoEnum.DISPONIVEL.value:
                raise ValueError(f"Assento {seat.id} não está disponível para reserva")
            
        for seat in seats:
            seat.status = StatusAssentoEnum.RESERVADO.value
            updated_seats.append(seat)

        db.commit()

        return [self._to_response(seat) for seat in updated_seats]
    
    def get_seats_map(self, session_id: int) -> dict:
        seats = self.search_seats_by_session(session_id)

        map = {}
        for seat in seats:
            row = seat.codigo[0]

            if row not in map:
                map[row] = []

            map[row].append({
                'id': seat.id,
                'codigo': seat.codigo,
                'tipo': seat.tipo,
                'preco': seat.preco,
                'status': seat.status,
                'posicao_x': seat.posicao_x,
                'posicao_y': seat.posicao_y
            })

        for row in map:
            map[row].sort(key=lambda x: x['posicao_x'] or 0)

        return map
    
    # =================== Métodos Privados =================== #

    def _update_seat_status(self, db: Session, seat_id: int, new_status: StatusAssentoEnum) -> AssentoResponse:
        seat = db.query(Assento).filter(Assento.id == seat_id).first()
        if not seat:
            raise ValueError("Assento não encontrado")
        
        if not self._validate_status_transition(seat.status, new_status.value):
            raise ValueError(f"Transição de status inválida de {seat.status} para {new_status.value}")
        
        seat.status = new_status.value
        db.commit()
        db.refresh(seat)

        return self._to_response(seat)
    
    def _validate_status_transition(self, actual_status: str, new_status: str) -> bool:
        transitions = {
            StatusAssentoEnum.DISPONIVEL.value: [StatusAssentoEnum.RESERVADO.value, StatusAssentoEnum.INDISPONIVEL.value],
            StatusAssentoEnum.RESERVADO.value: [StatusAssentoEnum.OCUPADO.value, StatusAssentoEnum.DISPONIVEL.value],
            StatusAssentoEnum.OCUPADO.value: [StatusAssentoEnum.DISPONIVEL.value],
            StatusAssentoEnum.INDISPONIVEL.value: [StatusAssentoEnum.DISPONIVEL.value]
        }

        return new_status in transitions.get(actual_status, [])
    
    def _calculate_type_price(self, seat_type: str, base_price: float) -> float:
        multipliers = {
            "comum": 1.0,
            "vip": 1.5,
            "casal": 1.8,
            "premium": 2.0
        }

        return count(base_price * multipliers.get(seat_type.lower(), 1.0), 2)
    
    def _to_response(self, seat: Assento) -> AssentoResponse:
        return AssentoResponse(
            id=seat.id,
            sessao_id=seat.sessao_id,
            assento_sala_id=seat.assento_sala_id,
            preco=seat.preco,
            status=StatusAssentoEnum(seat.status),
            codigo=seat.codigo,
            tipo=seat.tipo,
            posicao_x=seat.posicao_x,
            posicao_y=seat.posicao_y
        )
    
    def _to_sessao_view(self, seat: Assento) -> AssentoSessaoView:
        return AssentoSessaoView(
            id=seat.id,
            codigo=seat.codigo,
            tipo=seat.tipo,
            preco=seat.preco,
            status=StatusAssentoEnum(seat.status),
            posicao_x=seat.posicao_x,
            posicao_y=seat.posicao_y
        )
    
assento_service = AssentoService()