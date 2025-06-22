from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.assento_schema import AssentoCreate, AssentoResponse, AssentoSessaoView, AssentoUpdate
from app.service.assento_service import assento_service


router = APIRouter(
    prefix="/seats",
    tags=["Seats"],
)

@router.get(
    "/session/{session_id}",
    response_model=List[AssentoSessaoView],
    description="Obter assentos disponíveis para uma sessão específica",
    status_code=status.HTTP_200_OK
)
def get_session_seats(
    session_id: int,
    only_active: bool = Query(False, description="Filtrar apenas assentos disponíveis"),
    db: Session = Depends(get_db),
):
    try:
        seats = assento_service.get_seats_by_session(
            db=db,
            session_id=session_id,
            only_active=only_active
        )

        return seats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    
@router.get(
    "/session/{session_id}/map",
    status_code=status.HTTP_200_OK,
)
def get_seats_map(
    session_id: int,
    db: Session = Depends(get_db),
):
    try:
        seats_map = assento_service.get_seats_map(session_id)
        return seats_map
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )

@router.get(
    "/{session_id}",
    response_model=AssentoResponse,
)
def get_seat(
    session_id: int,
    db: Session = Depends(get_db),
):
    try:
        seat = assento_service.search_seat_by_id(db, session_id)

        if not seat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assento não encontrado"
            )
        
        return seat
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    
@router.patch(
    "/{seat_id}/reserve",
    response_model=AssentoResponse,
)
def reserve_seat(
    seat_id: int,
):
    try:
        reserved_seat = assento_service.reserve_seat(seat_id)

        return reserved_seat
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    
@router.patch(
    "/{seat_id}/occupy",
    response_model=AssentoResponse,
)
def occupy_seat(
    seat_id: int,
):
    try:
        return assento_service.occupy_seat(seat_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    
@router.patch(
    "/{seat_id}/liberate",
    response_model=AssentoResponse,
)
def liberate_seat(
    seat_id: int
):
    try:
        return assento_service.liberate_seat(seat_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    
@router.patch(
    "/{seat_id}/unliberate",
    response_model=AssentoResponse,
)
def unliberate_seat(
    seat_id: int
):
    try:
        return assento_service.unliberate_seat(seat_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    
@router.patch(
    "/reserve-multiple",
    response_model=List[AssentoResponse],
)
def reserve_multiple_seats(
    seat_ids: List[int],
    db: Session = Depends(get_db),
):
    try:
        reserved_seats = assento_service.reserve_many_seats(db, seat_ids)

        return reserved_seats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    
@router.post(
    "/",
    response_model=AssentoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_seat(
    seat_data: AssentoCreate,
    db: Session = Depends(get_db),
):
    try:
        new_seat = assento_service.create_seat(db, seat_data)

        return new_seat
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    
@router.put(
    "/{seat_id}",
    response_model=AssentoResponse,
    status_code=status.HTTP_200_OK,
)
def update_seat(
    seat_id: int,
    seat_data: AssentoUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated_seat = assento_service.update_seat(db, seat_id, seat_data)

        return updated_seat
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    
@router.delete(
    "/{seat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_seat(
    seat_id: int,
    db: Session = Depends(get_db),
):
    try:
        success = assento_service.delete_seat(db, seat_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Assento não encontrado"
            )
        
        return {"detail": "Assento excluído com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
)
    
@router.delete(
    "/session/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_seats_from_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    try:
        success = assento_service.delete_seats_from_session(db, session_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Sessão não encontrada ou sem assentos"
            )
        
        return {"detail": "Assentos excluídos com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )