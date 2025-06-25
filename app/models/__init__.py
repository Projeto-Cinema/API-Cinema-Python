from app.models.base import BaseModel
from app.models.usuario import Usuario
from app.models.endereco import Endereco
from app.models.cinema import Cinema
from app.models.sala import Sala
from app.models.filme import Filme
from app.models.genero import Genero
from app.models.sessao import Sessao
from app.models.assento_sala import AssentoSala
from app.models.reserva import Reserva, ItemReserva
from app.models.Produto import Produto
from app.models.pagamento import Pagamento

# Exporta todos os modelos para facilitar importações
__all__ = [
    "BaseModel",
    "Usuario",
    "Endereco",
    "Cinema",
    "Sala",
    "Filme",
    "Genero",
    "Sessao",
    "AssentoSala",
    "Reserva",
    "ItemReserva",
    "Produto",
    "Pagamento"
]