from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.filme_schema import FilmeCreate, FilmeResponse
from app.service.filme_service import filme_service


router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)

@router.post(
    "/",
    response_model=FilmeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo filme",
    description="Cria um novo filme com os dados fornecidos. Retorna os detalhes do filme criado.",
)
async def create_movie(
    movie_data: FilmeCreate,
    db: Session = Depends(get_db)
):
    return filme_service.create_movie(db, movie_data)