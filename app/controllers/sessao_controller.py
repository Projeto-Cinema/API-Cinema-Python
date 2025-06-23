from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.sessao_schema import SessaoCreate, SessaoResponse, SessaoUpdate
from app.service.sessao_service import sessao_service


router = APIRouter(
    prefix="/session",
    tags=["Session"],
)

@router.post(
    "/",
    response_model=SessaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova sessão de cinema",
    description="Cria uma nova sessão de cinema com os dados fornecidos.",
)
def create_session(
    session_data: SessaoCreate,
    db: Session = Depends(get_db)
):
    created_session = sessao_service.create_session(db, session_data)

    return created_session

@router.get(
    "/",
    response_model=list[SessaoResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtém todas as sessões de cinema",
    description="Obtém uma lista de todas as sessões de cinema, com suporte à paginação"
)
def get_all_sessions(
    skip: int = Query(0, ge=0, description="Número de sessões a serem puladas"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de sessões a serem retornadas"),
    db: Session = Depends(get_db),
):
    sessions = sessao_service.get_all_sessions(db, skip=skip, limit=limit)

    return sessions

@router.get(
    "/{session_id}",
    response_model=SessaoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém uma sessão de cinema por ID",
    description="Obtém os detalhes de uma sessão de cinema específica pelo seu ID."
)
def get_session_by_id(
    session_id: int,
    db: Session = Depends(get_db)
):
    session = sessao_service.get_session_by_id(db, session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sessão com id {session_id} não encontrada."
        )

    return session

@router.put(
    "/{session_id}",
    response_model=SessaoResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza uma sessão de cinema",
    description="Atualiza os dados de uma sessão de cinema existente pelo seu ID."
)
def update_session(
    session_id: int,
    session_data: SessaoUpdate,
    db: Session = Depends(get_db)
):
    updated_session = sessao_service.update_session(session_id, session_data, db)

    if not updated_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sessão com id {session_id} não encontrada."
        )

    return updated_session

@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma sessão de cinema",
    description="Deleta uma sessão de cinema existente pelo seu ID."
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    deleted_session = sessao_service.delete_session(db, session_id)

    if not deleted_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sessão com id {session_id} não encontrada."
        )

    return {"detail": "Sessão deletada com sucesso."}