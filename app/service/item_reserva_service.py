from typing import Optional
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from app.models.reserva import ItemReserva

class ItemReservaService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def search_item_by_id(self, db: Session, item_id: int) -> Optional[ItemReserva]:
        return db.query(ItemReserva).filter(ItemReserva.id == item_id).first()
    
item_reserva_service = ItemReservaService()