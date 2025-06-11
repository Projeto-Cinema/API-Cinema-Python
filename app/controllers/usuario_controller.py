from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
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

@router.get(
    "/cpf/{cpf}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_by_cpf(cpf: str, db: Session = Depends(get_db)):
    db_usuario = usuario_service.get_usuario_by_cpf(db, cpf)

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    return db_usuario

@router.get(
    "/",
    response_model=List[UsuarioResponse],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    skip: int = Query(0, ge=0, description="Número de registros a serem pulados"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros por página"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    tipo: Optional[bool] = Query(None, description="Filtrar por tipo de usuário"),
    db: Session = Depends(get_db)
):
    return usuario_service.get_usuarios(
        db,
        skip=skip,
        limit=limit,
        ativo=ativo,
        tipo=tipo
    )

@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    db_usuario = usuario_service.update_usuarios(db, usuario_id, usuario_data)

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    return db_usuario

@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def desactivate_user(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    success = usuario_service.delete_partial_user(db, usuario_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )