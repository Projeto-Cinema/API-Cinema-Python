from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from app.models.usuario import Usuario

class UsuarioService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> str:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_user(self, db: Session, usuario_data: UsuarioCreate) -> Usuario:
        try:
            hashed_password = self._hash_password(usuario_data.senha)

            usuario_dict = usuario_data.model_dump(exclude={'senha'})
            usuario_dict['senha'] = hashed_password

            db_usuario = Usuario(**usuario_dict)
            db.add(db_usuario)
            db.commit()
            db.refresh(db_usuario)

            return db_usuario
        
        except IntegrityError as e:
            db.rollback()

            if "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado."
                )
            elif "cpf" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CPF já cadastrado."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar usuário."
                )
            
    def get_usuario_by_id(self, db: Session, usuario_id: int) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_usuario_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_usuario_by_cpf(self, db: Session, cpf: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.cpf == cpf).first()
    
    def get_usuarios(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        ativo: Optional[bool] = None,
        tipo: Optional[str] = None,
    ) -> List[Usuario]:
        query = db.query(Usuario)

        if ativo is not None:
            query = query.filter(Usuario.ativo == ativo)

        if tipo:
            query = query.filter(Usuario.tipo == tipo)

        return query.offset(skip).limit(limit).all()
    
    def update_usuarios(
        self,
        db: Session,
        usuario_id: int,
        usuario_data: UsuarioUpdate
    ) -> Optional[Usuario]:
        db_usuario = self.get_usuario_by_id(db, usuario_id)

        if not db_usuario:
            return None
        
        try:
            update_data = usuario_data.model_dump(exclude_unset=True)

            if 'senha' in update_data:
                update_data['senha'] = self._hash_password(update_data['senha'])

            for field, value in update_data.items():
                setattr(db_usuario, field, value)

            db.commit()
            db.refresh(db_usuario)

            return db_usuario
        
        except IntegrityError as e:
            db.rollback()

            if "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já está em uso."
                ) 
            elif "cpf" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CPF já está em uso."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro de integridade nos dados."
                )
            
    def delete_partial_user(self, db: Session, usuario_id: int) -> bool:
        db_usuario = self.get_usuario_by_id(db, usuario_id)

        if not db_usuario:
            return False
        
        db_usuario.ativo = False
        db.commit()

        return True
    
usuario_service = UsuarioService()