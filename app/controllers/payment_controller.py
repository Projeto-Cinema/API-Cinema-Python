from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions.custom_exceptions import NotFoundError, ValidationError
from app.models.schemas.pagamento_schema import PagamentoCreate, PagamentoResponse
from app.service.pagamento_service import payment_service


router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)

@router.post(
    "/",
    response_model=PagamentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Payment",
    description="Create a new payment for a reservation."
)
async def create_payment(
    payment_data: PagamentoCreate,
    db: Session = Depends(get_db)
):
    try:
        payment = payment_service.create_payment(payment_data, db)
        return payment
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/{payment_id}",
    response_model=PagamentoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Payment by ID",
    description="Retrieve a payment by its ID."
)    
async def get_payment_by_id(
    payment_id: int,
    db: Session = Depends(get_db)
):
    try:
        payment = payment_service.get_payment_by_id(payment_id, db)
        return payment
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )