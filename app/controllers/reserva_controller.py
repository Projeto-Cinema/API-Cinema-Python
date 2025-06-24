from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.reserva_schema import ReservaCreate, ReservaResponse
from app.service.reserva_service import reserva_service


router = APIRouter(
    prefix="/reservas",
    tags=["Reservation"]
)

@router.post(
    "/",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED
)
def create_reserve(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db)
):
    try:
        return reserva_service.create_reservation(db, reserva_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/{reserva_id}",
    response_model=ReservaResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca uma reserva pelo ID",
    description="Retorna os detalhes de uma reserva específica com base no ID fornecido.",
)
def get_reservation_by_id(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = reserva_service.get_reservation_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva não encontrada."
        )
    return reserva

@router.get(
    "/codigo/{codigo}",
    response_model=ReservaResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca uma reserva pelo código",
    description="Retorna os detalhes de uma reserva específica com base no código fornecido.",
)
def get_reservation_by_code(
    codigo: str,
    db: Session = Depends(get_db)
):
    reserva = reserva_service.get_reservation_by_code(db, codigo)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva não encontrada."
        )
    return reserva

@router.get(
    "/usuario/{usuario_id}",
    response_model=list[ReservaResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista reservas por usuário",
    description="Retorna todas as reservas feitas por um usuário específico com base no ID do usuário.",
)
def list_reservations_by_user(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    reservas = reserva_service.list_reservations_by_user(db, usuario_id)
    if not reservas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma reserva encontrada para o usuário."
        )
    return reservas