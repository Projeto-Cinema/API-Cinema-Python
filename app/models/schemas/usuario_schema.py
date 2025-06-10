from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional

import re

class UsuarioBase(BaseModel):
    nome: str
    email: str
    dt_nascimento: Optional[datetime] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    ativo: bool = True
    tipo: str = "cliente"

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email é obrigatório')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Formato de email inválido')
        
        return v

class UsuarioCreate(UsuarioBase):
    senha: str

    @field_validator('senha')
    @classmethod
    def validate_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        
        return v

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    dt_nascimento: Optional[datetime] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    ativo: Optional[bool] = None
    tipo: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email é obrigatório')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Formato de email inválido')
        
        return v
    
    @field_validator('senha')
    @classmethod
    def validate_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        
        return v

class UsuarioAuthenticate(BaseModel):
    email: str
    senha: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email é obrigatório')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Formato de email inválido')
        
        return v

class UsuarioResponse(UsuarioBase):
    id: int
    dt_cadastro: datetime
    ultimo_acesso: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }