from fastapi import APIRouter, Depends, HTTPException, Query, status

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

@router.get(
    "/{movie_id}",
    response_model=FilmeResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém filme por ID",
    description="Obtém os detalhes de um filme específico pelo ID fornecido. Retorna um erro 404 se o filme não for encontrado.",
)
async def get_movie_by_id(
    movie_id: int,
    db: Session = Depends(get_db)
):
    db_movie = filme_service.get_movie_by_id(db, movie_id)

    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado."
        )
    
    return db_movie

@router.get(
    "/",
    response_model=FilmeResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém filme por título",
    description="Obtém os detalhes de um filme específico pelo título fornecido. Retorna um erro 404 se o filme não for encontrado.",
)
async def get_movie_by_title(
    title: str = Query(..., alias='titulo'),
    db: Session = Depends(get_db)
):
    db_movie = filme_service.get_movie_by_title(db, title)

    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado."
        )
    
    return db_movie