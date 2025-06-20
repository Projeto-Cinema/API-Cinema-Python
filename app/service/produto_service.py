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
        
produto_service = ProdutoService()