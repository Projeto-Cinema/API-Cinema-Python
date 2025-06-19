from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.cinema_schema import CinemaCreate, CinemaResponse, CinemaUpdate
from app.service.cinema_service import cinema_service


router = APIRouter(
    prefix="/cinema",
    tags=["cinema"],
)

@router.post(
    "/",
    response_model=CinemaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo cinema",
    description="Cria um novo cinema com os dados fornecidos. Retorna os detalhes do cinema"
)
async def create_cinema(
    cinema: CinemaCreate,
    db: Session = Depends(get_db)
):
    return cinema_service.create_cinema(db, cinema)

@router.get(
    "/{cinema_id}",
    response_model=CinemaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém cinema por ID",
    description="Obtém os detalhes de um cinema específico pelo ID fornecido. Retorna um erro 404 se o cinema não for encontrado."
)
async def get_cinema_by_id(
    cinema_id: int,
    db: Session = Depends(get_db)
):
    db_cinema = cinema_service.get_cinema_by_id(db, cinema_id)

    if not db_cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cinema não encontrado."
        )
    
    return db_cinema

@router.get(
    "/name/{name}",
    response_model=CinemaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém cinema por nome",
    description="Obtém os detalhes de um cinema específico pelo nome fornecido. Retorna um erro 404 se o cinema não for encontrado."
)
async def get_cinema_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    db_cinema = cinema_service.get_cinema_by_name(db, name)

    if not db_cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cinema não encontrado."
        )
    
    return db_cinema

@router.get(
    "/",
    response_model=List[CinemaResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtém todos os cinemas",
    description="Obtém uma lista de todos os cinemas cadastrados. Permite filtragem por status ativo/inativo, com paginação."
)
async def get_cinemas(
    skip: int = Query(0, ge=0, description="Número de registros a serem pulados"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a serem retornados"),
    ativo: Optional[bool] = Query(None, description="Filtrar cinemas ativos ou inativos"),
    db: Session = Depends(get_db)
):
    return cinema_service.get_cinemas(
        db,
        skip=skip,
        limit=limit,
        ativo=ativo
    )

@router.put(
    "/{cinema_id}",
    response_model=CinemaResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza cinema",
    description="Atualiza os dados de um cinema existente. Retorna os detalhes atualizados do cinema."
)
async def update_cinema(
    cinema_id: int,
    cinema_data: CinemaUpdate,
    db: Session = Depends(get_db)
):
    db_cinema = cinema_service.update_cinema(db, cinema_id, cinema_data)

    if not db_cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cinema não encontrado."
        )
    
    return db_cinema