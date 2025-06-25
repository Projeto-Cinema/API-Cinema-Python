from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_admin_user
from app.models.schemas.endereco_schema import EnderecoCreate, EnderecoResponse, EnderecoUpdate
from app.service.endereco_service import endereco_service


router = APIRouter(
    prefix="/address",
    tags=["Address"],
)

@router.post(
    "/",
    response_model=EnderecoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo endereço",
    description="Cria um novo endereço com os dados fornecidos",
)
async def create_address(
    address: EnderecoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    return endereco_service.create_endereco(db, address)

@router.get(
    "/{usuario_id}",
    response_model=EnderecoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém endereço por ID",
    description="Obtém os detalhes de um endereço específico pelo ID fornecido. Retorna um erro 404 se o endereço não for encontrado.",
)
async def get_address_by_id(
        usuario_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_admin_user)
    ):
    db_endereco = endereco_service.get_address_by_id(db, usuario_id)

    if not db_endereco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endereço não encontrado."
        )
    
    return db_endereco

@router.get(
    "/cep/{cep}",
    response_model=EnderecoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém endereço por CEP",
    description="Obtém os detalhes de um endereço específico pelo CEP fornecido. Retorna um erro 404 se o endereço não for encontrado.",
)
async def get_address_by_cep(
        cep: str,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_admin_user)
    ):
    db_endereco = endereco_service.get_address_by_cep(db, cep)

    if not db_endereco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endereço não encontrado."
        )
    
    return db_endereco

@router.get(
    "/",
    response_model=List[EnderecoResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtém lista de endereços",
    description="Obtém uma lista de endereços com paginação. Retorna até 100 endereços por padrão.",
)
async def get_addresses(
    skip: int = Query(0, ge=0, description="Número de registros a serem pulados"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a serem retornados"), 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    return endereco_service.get_all(db, skip=skip, limit=limit)

@router.put(
    "/{address_id}",
    response_model=EnderecoResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza um endereço",
    description="Atualiza os dados de um endereço existente com os dados fornecidos",
)
async def update_address(
    address_id: int,
    address_data: EnderecoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    db_address = endereco_service.update_address(db, address_id, address_data)

    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endereço não encontrado."
        )
    
    return db_address

@router.delete(
    "/delete/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um endereço",
    description="Deleta um endereço existente pelo ID fornecido. Retorna um erro 404 se o endereço não for encontrado.",
)
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    success = endereco_service.delete_address(db, address_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endereço não encontrado."
        )
    
    return {"detail": "Endereço deletado com sucesso."}