import secrets
import string
from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from app.models.reserva import ItemReserva, Reserva
from app.models.schemas.item_reserva_schema import ItemReservaCreate
from app.models.schemas.reserva_schema import ReservaCreate, ReservaUpdate
from app.models.sessao import Sessao
from app.models.usuario import Usuario

class ReservaService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def _generate_reserve_code(self, db: Session) -> str:
        while True:
            code = ''.join(secrets.choices(string.ascii_uppercase + string.digits, k=8))
            if not db.query(Reserva).filter(Reserva.codigo == code).first():
                return code
            
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
        if not self._validate_if_exists_user(db, reserve_data.usuario_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        
        if not self._validate_if_exists_session(db, reserve_data.sessao_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada."
            )
        
        if reserve_data.itens:
            total_value = self._calculate_total_item_value(reserve_data.items)
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
            metodo_pagamento=reserve_data.metodo_pagamento,
            assentos=reserve_data.assentos
        )

        db.add(reserve)
        db.flush()

        for item_data in reserve_data.itens:
            item = ItemReserva(
                reserva_id=reserve.id,
                item_id=item_data.item_id,
                tipo=item_data.tipo,
                quantidade=item_data.quantidade,
                preco_unitario=item_data.preco_unitario,
                preco_total=item_data.preco_total,
                desconto=item_data.desconto
            )
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
    
reserva_service = ReservaService()