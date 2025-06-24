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