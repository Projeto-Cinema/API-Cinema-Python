from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas.endereco_schema import EnderecoCreate, EnderecoResponse
from app.service.endereco_service import endereco_service


router = APIRouter(
    prefix="/address",
    tags=["Address"],
)

@router.post(
    "/",
    response_model=EnderecoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo endereço",
    description="Cria um novo endereço com os dados fornecidos",
)
async def create_address(
    address: EnderecoCreate,
    db: Session = Depends(get_db)
):
    return endereco_service.create_endereco(db, address)