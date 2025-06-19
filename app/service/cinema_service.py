from typing import Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.cinema import Cinema
from app.models.schemas.cinema_schema import CinemaCreate

class CinemaService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_cinema(self, db: Session, cinema_data: CinemaCreate) -> Cinema:
        try:
            cinema_dict = cinema_data.model_dump()

            db_cinema = Cinema(**cinema_dict)
            db.add(db_cinema)
            db.commit()
            db.refresh(db_cinema)

            return db_cinema
        
        except IntegrityError as e:
            db.rollback()

            if "cnpj" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CNPJ já cadastrado."
                )
            elif "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar cinema."
                )
            
    def get_cinema_by_id(self, db: Session, cinema_id: int) -> Optional[Cinema]:
        return db.query(Cinema).filter(Cinema.id == cinema_id).first()

cinema_service = CinemaService()