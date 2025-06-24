from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.item_reserva_schema import ItemReservaCreate, ItemReservaResponse

from app.service.item_reserva_service import item_reserva_service

router = APIRouter(
    prefix="/item_reserva",
    tags=["item_reserva"],
)

@router.get(
    "/{reserve_id}/itens",
    response_model=List[ItemReservaResponse],
    summary="Search Item Reserva by ID",
    description="Retrieve an item reserva by its ID.",
)
def search_item_reserve(
    reserve_id: int,
    db: Session = Depends(get_db)
):
    itens = item_reserva_service.search_item_by_id(db, reserve_id)

    return [ItemReservaResponse.from_orm(item) for item in itens]

@router.post(
    "/{reserve_id}/itens",
    response_model=ItemReservaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar Item Reserva",
    description="Adiciona um item reserva a uma reserva existente.",
)
def add_item_reserve(
    reserve_id: int,
    item_data: ItemReservaCreate,
    db: Session = Depends(get_db)       
):
    try:
        item = item_reserva_service.add_item_reserve(reserve_id, item_data, db)
        return ItemReservaResponse.from_orm(item)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))