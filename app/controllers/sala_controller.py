from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.sala_schema import SalaCreate, SalaResponse
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