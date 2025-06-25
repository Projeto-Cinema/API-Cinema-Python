from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_active_user, get_current_admin_user
from app.exceptions.custom_exceptions import NotFoundError, ValidationError
from app.models.schemas.pagamento_schema import PagamentoCreate, PagamentoResponse, PagamentoUpdate
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    if status:
        payments = payment_service.get_all_payments_by_status(db, status, skip, limit)
    else:
        payments = payment_service.get_all_payments(db, skip, limit)

    return payments

@router.put(
    "/{payment_id}",
    response_model=PagamentoResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Payment",
    description="Update an existing payment by its ID."
)
async def update_payment(
    payment_id: int,
    payment_data: PagamentoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        payment = payment_service.update_payment(payment_id, payment_data, db)
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
    
@router.post(
    "/{payment_id}/process",
    response_model=PagamentoResponse,
    status_code=status.HTTP_200_OK,
    summary="Process Payment",
    description="Process a payment by its ID, updating its status and processing details."
)
async def process_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        payment = payment_service.process_payment(payment_id, db)
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
    "{payment_id}/verify",
    response_model=PagamentoResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify Payment Status",
    description="Verify the status of a payment by its ID and return the payment details."
)
async def verify_payment_status(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        status_payment = payment_service.get_payment_by_id(payment_id, db)
        return status_payment
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
@router.get(
    "/{payment_id}/voucher",
    status_code=status.HTTP_200_OK,
    summary="Generate Voucher",
    description="Generate a voucher for a payment by its ID if the payment is approved."
)
async def generate_voucher(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        voucher = payment_service.generate_voucher(payment_id, db)
        return voucher
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
    
@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Payment",
    description="Delete a payment by its ID."
)
async def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    try:
        payment_service.delete_payment(payment_id, db)

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