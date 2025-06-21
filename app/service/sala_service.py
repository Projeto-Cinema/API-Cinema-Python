from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Sala
from app.models.schemas.sala_schema import SalaCreate

class SalaService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_room(self, db: Session, room_data: SalaCreate) -> Sala:
        try:
            room_dict = room_data.model_dump()
            
            db_room = Sala(**room_dict)
            db.add(db_room)
            db.commit()
            db.refresh(db_room)

            return db_room
        
        except IntegrityError as e:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar sala."
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
        
sala_service = SalaService()