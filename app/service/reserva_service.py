import random
import string
from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from app.models.assento_sala import AssentoSala
from app.models.reserva import ItemReserva, Reserva
from app.models.schemas.enum.enum_util import StatusReservaEnum
from app.models.schemas.item_reserva_schema import ItemReservaCreate
from app.models.schemas.reserva_schema import ReservaCreate, ReservaUpdate
from app.models.sessao import Sessao
from app.models.usuario import Usuario

class ReservaService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def _generate_reserve_code(self, db: Session) -> str:
        while True:
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            if not db.query(Reserva).filter(Reserva.codigo == code).first():
                return code

    def _get_user_or_404(self, db: Session, user_id: int) -> Usuario:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        return user
    
    def _get_session_or_404(self, db: Session, session_id: int) -> Sessao:
        session = db.query(Sessao).filter(Sessao.id == session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada."
            )
        return session
    
    def _validate_itens(self, db: Session, session: Sessao, itens: List[ItemReservaCreate]) -> float:
        value_total = 0.0

        for item_data in itens:
            if item_data.tipo == "assento":
                seat = db.query(AssentoSala).filter(AssentoSala.id == item_data.item_id).first()

                if not seat:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Assento com ID {item_data.item_id} não encontrado."
                    )
                
                if seat.is_session_reserved(session.id):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Assento {seat.numero} já está reservado para esta sessão."
                    )
                
                correct_price = session.calculate_seat_price(seat.id)
                if abs(correct_price - item_data.preco_unitario) > 0.01:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Preço incorreto para o assento {seat.numero}. Esperado: {correct_price}, recebido: {item_data.preco_unitario}."
                    )
                
            value_total += item_data.preco_total

        return value_total
            
    def _calculate_total_item_value(self, itens: List[ItemReservaCreate]) -> float:
        total = 0

        for item in itens:
            price_with_descount = item.preco_unitario - item.desconto
            total += price_with_descount * item.quantidade

        return total
    
    def _validate_if_exists_user(self, db: Session, usuario_id: int) -> Usuario:
        return db.query(Usuario).filter(Usuario.id == usuario_id).first() is not None
    
    def _validate_if_exists_session(self, db: Session, sessao_id: int) -> Sessao:
        return db.query(Sessao).filter(Sessao.id == sessao_id).first() is not None
    
    def create_reservation(self, db: Session, reserve_data: ReservaCreate) -> Reserva:
        self._get_user_or_404(db, reserve_data.usuario_id)
        session = self._get_session_or_404(db, reserve_data.sessao_id)
        
        if reserve_data.itens:
            total_value = self._validate_itens(db, session, reserve_data.itens)
            if abs(total_value - reserve_data.valor_total) > 0.01:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="O valor total não corresponde à soma dos itens."
                )
        
        reserve = Reserva(
            usuario_id=reserve_data.usuario_id,
            sessao_id=reserve_data.sessao_id,
            codigo=self._generate_reserve_code(db),
            data_reserva=reserve_data.data_reserva,
            status=reserve_data.status.value,
            valor_total=reserve_data.valor_total,
            metodo_pagamento=reserve_data.metodo_pagamento
        )

        db.add(reserve)
        db.flush()

        for item_data in reserve_data.itens:
            item = ItemReserva(**item_data.dict(), reserva_id=reserve.id)
            db.add(item)

        db.commit()
        db.refresh(reserve)

        return reserve
    
    def get_reservation_by_id(self, db: Session, reserva_id: int) -> Optional[Reserva]:
        return db.query(Reserva).filter(Reserva.id == reserva_id).first()

    def get_reservation_by_code(self, db: Session, codigo: str) -> Optional[Reserva]:
        return db.query(Reserva).filter(Reserva.codigo == codigo).first()
    
    def list_reservation_by_user(
        self, 
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Reserva]:
        return (
            db.query(Reserva)
                .filter(Reserva.usuario_id == user_id)
                .offset(skip)
                .limit(limit)
                .all()
        )
    
    def update_reservation(
        self,
        reservation_id: int,
        reserve_update: ReservaUpdate,
        db: Session
    ) -> Optional[Reserva]:
        reserve = self.get_reservation_by_id(db, reservation_id)

        if not reserve:
            return None
        
        update_data = reserve_update.dict(exclude_unset=True)

        if 'status' in update_data and update_data['status']:
            update_data['status'] = update_data['status'].value

        for field, value in update_data.items():
            setattr(reserve, field, value)

        db.commit()
        db.refresh(reserve)

        return reserve
    
    def cancel_reservation(
        self,
        reservation_id: int,
        db: Session
    ) -> Optional[Reserva]:
        reserve = self.get_reservation_by_id(db, reservation_id)
        if not reserve:
            return None
        
        if reserve.status == StatusReservaEnum.CANCELADA.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reserva já está cancelada."
            )
        
        if reserve.status == StatusReservaEnum.CONFIRMADA.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reserva confirmada não pode ser cancelada."
            )
        
        reserve.status = StatusReservaEnum.CANCELADA.value
        db.commit()
        db.refresh(reserve)

        return reserve

    def confirm_reservation(
        self,
        reservation_id: int,
        metodo: str,
        db: Session
    ) -> Optional[Reserva]:
        reserve = self.get_reservation_by_id(db, reservation_id)
        if not reserve:
            return None
        
        if reserve.status != StatusReservaEnum.PENDENTE.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas reservas pendentes podem ser confirmadas."
            )
        
        reserve.status = StatusReservaEnum.CONFIRMADA.value
        reserve.metodo_pagamento = metodo

        db.commit()
        db.refresh(reserve)

        return reserve
    
    def delete_reservation(
        self,
        reservation_id: int,
        db: Session
    ) -> True:
        reserve = self.get_reservation_by_id(db, reservation_id)
        if not reserve:
            return None
        
        if reserve.status == StatusReservaEnum.CONFIRMADA.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nãoe é possível excluir uma reserva confirmada."
            )

        db.delete(reserve)
        db.commit()

        return True
    
reserva_service = ReservaService()