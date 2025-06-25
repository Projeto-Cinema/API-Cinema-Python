from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.service.usuario_service import usuario_service


router = APIRouter(
    prefix="/Users",
    tags=["Users"],
)

@router.post(
    "/", 
    response_model=UsuarioResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário",
    description="Cria um novo usuário com os dados fornecidos. Retorna os detalhes do usuário criado.",
)
async def create_user(
    user: UsuarioCreate,
    db: Session = Depends(get_db)
):
    return usuario_service.create_user(db, user)

@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém usuário por ID",
    description="Obtém os detalhes de um usuário específico pelo ID fornecido. Retorna um erro 404 se o usuário não for encontrado.",
)
async def get_user_by_id(
    usuario_id: int, 
    current_user = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
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
    status_code=status.HTTP_200_OK,
    summary="Obtém usuário por email",
    description="Obtém os detalhes de um usuário específico pelo email fornecido. Retorna um erro 404 se o usuário não for encontrado.",
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
    status_code=status.HTTP_200_OK,
    summary="Obtém usuário por CPF",
    description="Obtém os detalhes de um usuário específico pelo CPF fornecido. Retorna um erro 404 se o usuário não for encontrado.",
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
    summary="Obtém lista de usuários",
    description="Obtém uma lista de usuários com opções de paginação e filtragem. Retorna uma lista de usuários ativos ou inativos, dependendo dos parâmetros fornecidos.",
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
    status_code=status.HTTP_200_OK,
    summary="Atualiza usuário",
    description="Atualiza os detalhes de um usuário existente com os dados fornecidos. Retorna os detalhes do usuário atualizado.",
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
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta usuário parcialmente (soft delete)",
    description="Deleta parcialmente um usuário, marcando-o como inativo. Retorna um erro 404 se o usuário não for encontrado.",
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
    
@router.delete(
    "/delete/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar usuário permanentemente",
    description="Deleta um usuário permanentemente do sistema. Retorna um erro 404 se o usuário não for encontrado.",
)
async def delete_user(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    success = usuario_service.delete_permanent_user(db, usuario_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    return {"detail": "Usuário deletado com sucesso."}

@router.patch(
    "/{usuario_id}/deactivate",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Desativar usuário (soft delete)",
    description="Desativa um usuário, marcando-o como inativo. Retorna os detalhes do usuário desativado.",
)
async def deactivate_user(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    db_usuario = usuario_service.deactivate_usuario(db, usuario_id)

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    return db_usuario

@router.patch(
    "/{usuario_id}/activate",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Ativar usuário",
    description="Ativa um usuário previamente desativado. Retorna os detalhes do usuário ativado.",
)
async def activate_user(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    db_usuario = usuario_service.activate_usuario(db, usuario_id)

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    return db_usuario
