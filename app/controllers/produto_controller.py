from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.service.produto_service import produto_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post(
    "/",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo produto",
    description="Cria um novo produto com os dados fornecidos. Retorna os detalhes do"
)
async def create_product(
    product: ProdutoCreate,
    db: Session = Depends(get_db)
):
    return produto_service.create_product(db, product)