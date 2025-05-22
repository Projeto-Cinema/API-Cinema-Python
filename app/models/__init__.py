from app.models.base import BaseModel
from app.models.usuario import Usuario, Endereco
from app.models.cinema import Cinema, Sala
from app.models.filme import Filme
from app.models.sessao import Sessao, Assento
from app.models.reserva import Reserva, ItemReserva
from app.models.Produto import Produto, Pagamento

# Exporta todos os modelos para facilitar importações
__all__ = [
    "BaseModel",
    "Usuario",
    "Endereco",
    "Cinema",
    "Sala",
    "Filme",
    "Sessao",
    "Assento",
    "Reserva",
    "ItemReserva",
    "Produto",
    "Pagamento"
]