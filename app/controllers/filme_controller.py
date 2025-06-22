from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.filme_schema import FilmeCreate, FilmeResponse, FilmeUpdate
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
    "/all",
    response_model=list[FilmeResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtém todos os filmes",
    description="Obtém uma lista de todos os filmes, com opções de paginação e filtros por status, diretor, classificação e ano de lançamento.",
)
async def get_all_movies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a serem pulados para paginação"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a serem retornados"),
    em_cartaz: Optional[bool] = Query(None, description="Filtrar filmes em cartaz (True) ou não (False), se fornecido"),
    diretor: Optional[str] = Query(None, description="Filtrar filmes por nome do diretor"),
    classificacao: Optional[str] = Query(None, description="Filtrar filmes por classificação"),
    ano_lancamento: Optional[int] = Query(None, description="Filtrar filmes por ano de lançamento")
):
    return filme_service.get_all_movies(
        db,
        skip=skip,
        limit=limit,
        em_cartaz=em_cartaz,
        diretor=diretor,
        classificacao=classificacao,
        ano_lancamento=ano_lancamento
    )

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

@router.put(
    "/{movie_id}",
    response_model=FilmeResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza um filme",
    description="Atualiza os dados de um filme existente pelo ID fornecido. Retorna os detalhes do filme atualizado.",
)
async def update_movie(
    movie_id: int,
    movie_data: FilmeUpdate,
    db: Session = Depends(get_db)
):
    db_movie = filme_service.update_movie(db, movie_id, movie_data)

    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado."
        )
    
    return db_movie

@router.delete(
    "/delete/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete permanente de filme",
    description="Deleta permanentemente um filme pelo ID fornecido. Retorna 204 No Content se a operação for bem-sucedida.",
)
async def delete_permanent_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    success = filme_service.delete_permanent_movie(db, movie_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado."
)