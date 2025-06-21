from pydantic import BaseModel


class Genero(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True