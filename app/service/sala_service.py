from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Sala
from app.models.assento_sala import AssentoSala
from app.models.cinema import Cinema
from app.models.schemas.enum.enum_util import StatusSalaEnum
from app.models.schemas.sala_schema import SalaCreate, SalaUpdate

class SalaService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_room(self, db: Session, room_data: SalaCreate) -> Sala:
        cinema = db.query(Cinema).filter(Cinema.id == room_data.cinema_id).first()
        if not cinema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cinema com id {room_data.cinema_id} não encontrado."
            )
        
        seat_data = room_data.assentos
        room_dict = room_data.model_dump(exclude={"assentos"})

        db_room = Sala(**room_dict)

        try:
            db.add(db_room)
            db.flush()

            for seat in seat_data:
                db_seat = AssentoSala(
                    **seat.dict(),
                    sala_id=db_room.id
                )
                db.add(db_seat)

            db.commit()
            db.refresh(db_room)

            return db_room
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar sala. Verifique os dados informados."
            )
        
    def get_room_by_id(self, db: Session, room_id: int) -> Optional[Sala]:
        return db.query(Sala).filter(Sala.id == room_id).first()
    
    def get_all_rooms(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        ativo: Optional[bool] = None
    ) -> List[Sala]:
        query = db.query(Sala)

        if ativo is not None:
            query = query.filter(Sala.status == ativo)

        return query.offset(skip).limit(limit).all()
    
    def update_room(
        self,
        db: Session,
        room_id: int,
        room_data: SalaUpdate
    ) -> Optional[Sala]:
        db_room = self.get_room_by_id(db, room_id)

        if not db_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala não encontrada."
            )

        try:
            room_dict = room_data.model_dump(exclude_unset=True)
            for key, value in room_dict.items():
                setattr(db_room, key, value)

            db.add(db_room)
            db.commit()
            db.refresh(db_room)

            return db_room
        
        except IntegrityError as e:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar sala."
            )
        
    def parcial_delete_room(self, db: Session, room_id: int) -> bool:
        db_room = self.get_room_by_id(db, room_id)

        if not db_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala não encontrada."
            )

        db_room.status = StatusSalaEnum.INATIVO
        db.add(db_room)
        db.commit()

        return True
    
    def delete_room(self, db: Session, room_id: int) -> bool:
        db_room = self.get_room_by_id(db, room_id)

        if not db_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala não encontrada."
            )

        db.delete(db_room)
        db.commit()

        return True
        
sala_service = SalaService()