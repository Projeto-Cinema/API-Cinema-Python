from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.service.usuario_service import usuario_service


router = APIRouter(
    prefix="/Users",
    tags=["Users"],
)

@router.post(
    "/", 
    response_model=UsuarioResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UsuarioCreate,
    db: Session = Depends(get_db)
):
    return usuario_service.create_user(db, user)

@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_by_id(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = usuario_service.get_usuario_by_id(db, usuario_id)

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    return db_usuario

@router.get(
    "/email/{email}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_usuario = usuario_service.get_usuario_by_email(db, email)

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    return db_usuario