from typing import List, Optional
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.exceptions.custom_exceptions import NotFoundError, ValidationError
from app.models.pagamento import Pagamento
from app.models.reserva import Reserva
from app.models.schemas.pagamento_schema import PagamentoCreate

class PagamentoService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_payment(
        self,
        payment_data: PagamentoCreate,
        db: Session
    ):
        reserve = db.query(Reserva).filter(Reserva.id == payment_data.reserva_id).first()
        if not reserve:
            raise NotFoundError(f"Reserva com ID {payment_data.reserva_id} não encontrada.")
        
        existing_payment = db.query(Pagamento).filter(
            Pagamento.reserva_id == payment_data.reserva_id
        ).first()

        if existing_payment:
            raise ValidationError(f"Valor do pagamento {payment_data.valor} não corresponde ao valor da reserva {reserve.valor_total}.")
        
        try:
            payment = Pagamento(**payment_data.model_dump())
            db.add(payment)
            db.commit()
            db.refresh(payment)

            return payment
        
        except IntegrityError as e:
            db.rollback()
            raise ValidationError("Erro de integridade ao criar pagamento")
        
    def get_payment_by_id(
        self,
        payment_id: int,
        db: Session
    ) -> Pagamento:
        payment = db.query(Pagamento).filter(Pagamento.id == payment_id).first()
        if not payment:
            raise NotFoundError(f"Pagamento com ID {payment_id} não encontrado.")
        return payment
    
    def get_payment_by_reservation_id(
        self,
        reservation_id: int,
        db: Session
    ) -> Optional[Pagamento]:
        return db.query(Pagamento).filter(Pagamento.reserva_id == reservation_id).first()
    
    def get_all_payments(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Pagamento]:
        return db.query(Pagamento).offset(skip).limit(limit).all()
    
    def get_payment_by_status(
        self,
        db: Session,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Pagamento]:
        return db.query(Pagamento).filter(Pagamento.status == status).offset(skip).limit(limit).all() 
        
payment_service = PagamentoService()