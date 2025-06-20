from fastapi import APIRouter, Depends, HTTPException, status

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

@router.get(
    "/{product_id}",
    response_model=ProdutoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém um produto por ID",
    description="Obtém os detalhes de um produto específico pelo seu ID."
)
async def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = produto_service.get_product_by_id(db, product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )
    
    return product

@router.get(
    "/name/{product_name}",
    response_model=ProdutoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém um produto por nome",
    description="Obtém os detalhes de um produto específico pelo seu nome."
)
async def get_product_by_name(
    product_name: str,
    db: Session = Depends(get_db)
):
    product = produto_service.get_product_by_name(db, product_name)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )
    
    return product