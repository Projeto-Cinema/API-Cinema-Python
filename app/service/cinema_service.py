from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.cinema import Cinema
from app.models.schemas.cinema_schema import CinemaCreate, CinemaUpdate

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
    
    def get_cinema_by_name(self, db: Session, name: str) -> Optional[Cinema]:
        return db.query(Cinema).filter(Cinema.nome == name).first()

    def get_cinemas(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        ativo: Optional[bool] = None
    ) -> List[Cinema]:
        query = db.query(Cinema)

        if ativo is not None:
            query = query.filter(Cinema.ativo == ativo)

        return query.offset(skip).limit(limit).all()
    
    def update_cinema(
        self,
        db: Session,
        cinema_id: int,
        cinema_data: CinemaUpdate
    ) -> Optional[Cinema]:
        db_cinema = self.get_cinema_by_id(db, cinema_id)

        if not db_cinema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cinema não encontrado."
            )

        try:
            for key, value in cinema_data.model_dump(exclude_unset=True).items():
                setattr(db_cinema, key, value)

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
                    detail="Erro ao atualizar cinema."
                )
            
    def parcial_delete_cinema(
        self,
        db: Session,
        cinema_id: int
    ) -> bool:
        db_cinema = self.get_cinema_by_id(db, cinema_id)

        if not db_cinema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cinema não encontrado."
            )

        db_cinema.ativo = False
        db.commit()
        
        return True

cinema_service = CinemaService()