from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.endereco import Endereco
from app.models.schemas.endereco_schema import EnderecoCreate

class EnderecoService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_endereco(self, db: Session, endereco_data: EnderecoCreate) -> Endereco:
        try:
            endereco_dict = endereco_data.model_dump()

            db_endereco = Endereco(**endereco_dict)
            db.add(db_endereco)
            db.commit()
            db.refresh(db_endereco)

            return db_endereco
        
        except IntegrityError as e:
            db.rollback()

            if "cep" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CEP já cadastrado."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar endereço."
                )
            
    def get_address_by_id(self, db: Session, endereco_id: int) -> Optional[Endereco]:
        return db.query(Endereco).filter(Endereco.id == endereco_id).first()
    
    def get_address_by_cep(self, db: Session, cep: str) -> Optional[Endereco]:
        return db.query(Endereco).filter(Endereco.cep == cep).first()
    
    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Endereco]:
        query = db.query(Endereco)

        return query.offset(skip).limit(limit).all()
    
endereco_service = EnderecoService()