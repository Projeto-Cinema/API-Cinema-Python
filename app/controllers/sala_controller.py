from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.sala_schema import SalaCreate, SalaResponse, SalaUpdate
from app.service.sala_service import sala_service


router = APIRouter(
    prefix="/room",
    tags=["Room"],
)

@router.post(
    "/",
    response_model=SalaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova sala",
    description="Cria uma nova sala com os dados fornecidos. Retorna os detalhes da sala criada.",
)
async def create_room(
    room: SalaCreate,
    db: Session = Depends(get_db)
):
    return sala_service.create_room(db, room)

@router.get(
    "/{room_id}",
    response_model=SalaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém sala por ID",
    description="Obtém os detalhes de uma sala específica pelo ID fornecido. Retorna um erro 404 se a sala não for encontrada.",
)
async def get_room_by_id(
    room_id: int,
    db: Session = Depends(get_db)
):
    db_room = sala_service.get_room_by_id(db, room_id)

    if not db_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala não encontrada."
        )
    
    return db_room

@router.get(
    "/",
    response_model=list[SalaResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtém todas as salas",
    description="Obtém uma lista de todas as salas, com opções de paginação e filtro por status ativo.",
)
async def get_all_rooms(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a serem pulados para paginação"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a serem retornados"),
    ativo: Optional[bool] = Query(None, description="Filtrar salas ativas (True) ou inativas (False), se fornecido")
):
    return sala_service.get_all_rooms(db, skip=skip, limit=limit, ativo=ativo)

@router.put(
    "/{room_id}",
    response_model=SalaResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza uma sala",
    description="Atualiza os dados de uma sala existente pelo ID fornecido. Retorna os detalhes da sala atualizada.",
)
async def update_room(
    room_id: int,
    room_data: SalaUpdate,
    db: Session = Depends(get_db)
):
    db_room = sala_service.update_room(db, room_id, room_data)

    if not db_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala não encontrada."
        )
    
    return db_room

@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft delete de sala",
    description="Realiza um soft delete de uma sala pelo ID fornecido. Retorna 204 No Content se a operação for bem-sucedida.",
)
async def soft_delete_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    success = sala_service.parcial_delete_room(db, room_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala não encontrada."
        )

@router.delete(
    "/delete/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Exclui sala permanentemente",
    description="Exclui uma sala permanentemente pelo ID fornecido. Retorna 204 No Content se a operação for bem-sucedida.",
)
async def delete_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    success = sala_service.delete_room(db, room_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala não encontrada."
        )