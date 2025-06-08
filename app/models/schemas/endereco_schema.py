from typing import Optional
from pydantic import BaseModel, Field


class EnderecoBase(BaseModel):
    cep: str
    logradouro: str
    numero: int = Field(ge=0)
    bairro: str
    cidade: str
    estado: str
    complemento: str
    referencia: str

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoUpdate(BaseModel):
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[int] = Field(None, ge=0)
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    complemento: Optional[str] = None
    referencia: Optional[str] = None

class EnderecoResponse(EnderecoBase):
    id: int

    class Config:
        from_attributes = True
        json_encoders = {
            str: lambda v: v if v else None
        }