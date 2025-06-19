from fastapi import APIRouter, Depends, status

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