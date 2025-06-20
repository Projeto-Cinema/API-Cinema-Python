from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Produto
from app.models.schemas.produto_schema import ProdutoCreate

class ProdutoService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_product(self, db: Session, product_data: ProdutoCreate) -> Produto:
        try:
            product_dict = product_data.model_dump()

            db_product = Produto(**product_dict)
            db.add(db_product)
            db.commit()
            db.refresh(db_product)

            return db_product
        
        except IntegrityError as e:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar produto."
            )
        
    def get_product_by_id(self, db: Session, product_id: int) -> Optional[Produto]:
        return db.query(Produto).filter(Produto.id == product_id).first()
    
    def get_product_by_name(self, db: Session, product_name: str) -> Optional[Produto]:
        return db.query(Produto).filter(Produto.nome == product_name).first()
    
    def get_products(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        ativo: Optional[bool] = None
    ) -> List[Produto]:
        query = db.query(Produto)

        if ativo is not None:
            query = query.filter(Produto.ativo == ativo)

        return query.offset(skip).limit(limit).all()
        
produto_service = ProdutoService()