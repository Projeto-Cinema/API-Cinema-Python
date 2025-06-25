from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session, joinedload

from app.models.sala import Sala
from app.models.schemas.sessao_schema import SessaoCreate, SessaoUpdate
from app.models.sessao import Sessao

class SessaoService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def _verify_time_conflict(
        self,
        db: Session,
        room_id: int,
        start_time: str,
        end_time: str,
        exclude_session_id: int = None
    ) -> Optional[Sessao]:
        query = db.query(Sessao).filter(
            Sessao.sala_id == room_id,
            Sessao.horario_ini < end_time,
            Sessao.horario_fim > start_time
        )

        if exclude_session_id:
            query = query.filter(Sessao.id != exclude_session_id)

        return query.first()
    
    def create_session(
        self,
        db: Session,
        session_data: SessaoCreate
    ) -> Sessao:
        sala = db.query(Sala).filter(Sala.id == session_data.sala_id).first()
        if not sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sala com id {session_data.sala_id} não encontrada."
            )
        
        if self._verify_time_conflict(
            db,
            session_data.sala_id,
            session_data.horario_ini,
            session_data.horario_fim
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflito de horário na sala."
            )
        
        session_dict = session_data.model_dump()
        db_session = Sessao(**session_dict)

        db.add(db_session)
        db.commit()
        db.refresh(db_session)

        return db_session
    
    def get_session_by_id(
        self,
        db: Session,
        session_id: int
    ) -> Optional[Sessao]:
        return db.query(Sessao).filter(Sessao.id == session_id).first()
    
    def get_all_sessions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Sessao]:
        return db.query(Sessao).offset(skip).limit(limit).all()
    
    def update_session(
        self,
        session_id: int,
        session_data: SessaoUpdate,
        db: Session
    ) -> Optional[Sessao]:
        db_session = self.get_session_by_id(db, session_id)
        if not db_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sessão com id {session_id} não encontrada."
            )
        
        updated_data = session_data.model_dump(exclude_unset=True)

        check_time = 'horario_ini' in updated_data or 'horario_fim' in updated_data
        if check_time:
            ini = updated_data.get('horario_ini', db_session.horario_ini)
            fim = updated_data.get('horario_fim', db_session.horario_fim)
            if self._verify_time_conflict(
                db,
                db_session.sala_id,
                ini,
                fim,
                exclude_session_id=session_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflito de horário na sala."
                )
            
            for key, value in updated_data.items():
                setattr(db_session, key, value)

            db.commit()
            db.refresh(db_session)

            return db_session
        
    def delete_session(
        self,
        db: Session,
        session_id: int
    ) -> Optional[Sessao]:
        db_session = self.get_session_by_id(db, session_id)
        if not db_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sessão com id {session_id} não encontrada."
            )
        
        db.delete(db_session)
        db.commit()

        return db_session
    
sessao_service = SessaoService()