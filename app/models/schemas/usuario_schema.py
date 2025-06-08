from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    dt_nascimento: Optional[datetime] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    ativo: bool = True
    tipo: str = "cliente"

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    dt_nascimento: Optional[datetime] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    ativo: Optional[bool] = None
    tipo: Optional[str] = None

class UsuarioAuthenticate(BaseModel):
    email: EmailStr
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    dt_cadastro: datetime
    ultimo_acesso: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }