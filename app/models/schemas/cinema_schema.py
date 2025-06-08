from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CinemaBase(BaseModel):
    nome: str
    cnpj: str
    telefone: Optional[str] = None
    email: EmailStr
    site : Optional[str] = None
    horario_func: Optional[str] = None
    imagem_url: Optional[str] = None
    ativo: bool = True

class CinemaCreate(CinemaBase):
    endereco_id: int
    
class CinemaUpdate(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    site : Optional[str] = None
    horario_func: Optional[str] = None
    imagem_url: Optional[str] = None
    ativo: Optional[bool] = None

class CinemaResponse(CinemaBase):
    id: int
    endereco_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }