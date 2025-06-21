from fastapi import APIRouter, Depends, status

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