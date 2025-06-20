from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.produto_schema import ProdutoCreate, ProdutoResponse, ProdutoUpdate
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

@router.get(
    "/",
    response_model=list[ProdutoResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtém uma lista de produtos",
    description="Obtém uma lista de produtos com opções de paginação e filtro por ativo."
)
async def get_products(
    skip: int = 0,
    limit: int = 100,
    ativo: bool = None,
    db: Session = Depends(get_db)
):
    return produto_service.get_products(
        db,
        skip=skip,
        limit=limit,
        ativo=ativo
    )

@router.put(
    "/{product_id}",
    response_model=ProdutoResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza um produto",
    description="Atualiza os detalhes de um produto existente pelo seu ID. Retorna os detalhes atualizados."
)
async def update_product(
    product_id: int,
    product_data: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    db_product = produto_service.update_product(db, product_id, product_data)

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )
    
    return db_product

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desativa um produto",
    description="Desativa um produto existente pelo seu ID. Retorna 204 No Content se a operação for bem-sucedida."
)
async def parcial_delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    success = produto_service.partial_delete_product(db, product_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )
    
    return {"detail": "Produto desativado com sucesso."}
