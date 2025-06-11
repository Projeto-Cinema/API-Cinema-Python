from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.usuario_schema import UsuarioCreate
from app.service.usuario_service import usuario_service


router = APIRouter(
    prefix="/Users",
    tags=["Users"],
)

@router.post(
    "/", 
    response_model=UsuarioCreate, 
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UsuarioCreate,
    db: Session = Depends(get_db)
):
    return usuario_service.create_user(db, user)