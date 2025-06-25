from datetime import timedelta
import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.usuario_schema import UsuarioAuthenticate
from app.service.auth_service import auth_service
from app.service.usuario_service import usuario_service


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/login",
    response_model=dict,
    summary="Login to get access token",
    description="This endpoint allows users to log in and receive an access token for authentication."
)
async def login_for_access_token(
    form_data: UsuarioAuthenticate,
    db: Session = Depends(get_db)
):
    user = usuario_service.get_usuario_by_email(db, form_data.email)

    if not user or not usuario_service._verify_password(form_data.senha, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.tipo},
        expires_delta=access_token_expires
    )

    user.ultimo_acesso = datetime.datetime.now()
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }