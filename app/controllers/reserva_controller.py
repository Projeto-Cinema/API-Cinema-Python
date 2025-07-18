from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_active_user, get_current_admin_user
from app.models.schemas.reserva_schema import ReservaCreate, ReservaResponse, ReservaUpdate
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
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
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    reservas = reserva_service.list_reservation_by_user(db, usuario_id)
    if not reservas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma reserva encontrada para o usuário."
        )
    return reservas

@router.put(
    "/{reserve_id}",
    response_model=ReservaResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza uma reserva",
    description="Atualiza os detalhes de uma reserva existente com base no ID fornecido.",
)
def update_reserve(
    reserve_id: int,
    reserve_data: ReservaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        reserve = reserva_service.update_reservation(db, reserve_id, reserve_data)
        if not reserve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva não encontrada."
            )

        return ReservaResponse.from_orm(reserve)
    
    except HTTPException as e:
        raise e
    
@router.patch(
    "/{reserve_id}/status",
    response_model=ReservaResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza o status de uma reserva",
    description="Atualiza o status de uma reserva existente com base no ID fornecido.",
)
def cancel_reservation(
    reserve_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        reserve = reserva_service.cancel_reservation(db, reserve_id)
        if not reserve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva não encontrada."
            )
        return ReservaResponse.from_orm(reserve)
    
    except HTTPException as e:
        raise e

@router.patch(
    "/{reserve_id}/confirm",
    response_model=ReservaResponse,
    status_code=status.HTTP_200_OK,
    summary="Confirma uma reserva",
    description="Confirma uma reserva existente com base no ID fornecido e o método de pagamento.",
)
def confirm_reservation(
    reserve_id: int,
    method: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        reserve = reserva_service.confirm_reservation(db, reserve_id, method)
        if not reserve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva não encontrada."
            )
        return ReservaResponse.from_orm(reserve)
    
    except HTTPException as e:
        raise e

@router.delete(
    "/{reserve_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Exclui uma reserva",
    description="Exclui uma reserva existente com base no ID fornecido.",
)    
def delete_reservation(
    reserve_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        result = reserva_service.delete_reservation(db, reserve_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva não encontrada."
            )
        return {"detail": "Reserva excluída com sucesso."}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
)