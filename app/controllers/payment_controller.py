from fastapi import APIRouter, Depends, HTTPException, Query, status

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

@router.get(
    "/reservation/{reservation_id}",
    response_model=PagamentoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Payment by Reservation ID",
    description="Retrieve a payment by its associated reservation ID."
)    
async def get_payment_by_reservation_id(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    payment = payment_service.get_payment_by_reservation_id(reservation_id, db)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment for reservation ID {reservation_id} not found."
        )
    return payment

@router.get(
    "/",
    response_model=list[PagamentoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get All Payments",
    description="Retrieve all payments with optional filtering by status."
)
async def get_all_payments(
    skip: int = Query(0, ge=0, description="Number of payments to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of payments to return"),
    status: str = Query(None, description="Filter payments by status"),
    db: Session = Depends(get_db)
):
    if status:
        payments = payment_service.get_all_payments_by_status(db, status, skip, limit)
    else:
        payments = payment_service.get_all_payments(db, skip, limit)

    return payments