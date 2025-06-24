from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.item_reserva_schema import ItemReservaResponse

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