import re
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class CinemaBase(BaseModel):
    nome: str
    cnpj: str
    telefone: Optional[str] = None
    email: str
    site : Optional[str] = None
    horario_func: Optional[str] = None
    imagem_url: Optional[str] = None
    ativo: bool = True

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email é obrigatório')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Formato de email inválido')
        
        return v

class CinemaCreate(CinemaBase):
    endereco_id: int
    
class CinemaUpdate(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
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