from enum import Enum


class StatusReservaEnum(str, Enum):
    PENDENTE = "Pendente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    EXPIRADA = "Expirada"

class TipoItemEnum(str, Enum):
    ASSENTO = "Assento"
    PRODUTO = "Produto"

class StatusSessaoEnum(str, Enum):
    ATIVA = "Ativa"
    INATIVA = "Inativa"
    CANCELADA = "Cancelada"

class StatusSalaEnum(str, Enum):
    ATIVA = "Ativa"
    INATIVA = "Inativa"
    CANCELADA = "Cancelada"

class StatusAssentoEnum(str, Enum):
    DISPONIVEL = "Disponível"
    RESERVADO = "Reservado"
    OCUPADO = "Ocupado"
    INDISPONIVEL = "Indisponível"