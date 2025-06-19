from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.cinema_schema import CinemaCreate, CinemaResponse
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