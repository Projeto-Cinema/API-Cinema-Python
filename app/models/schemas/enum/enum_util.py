from enum import Enum


class StatusReservaEnum(str, Enum):
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    EXPIRADA = "expirado"

class TipoItemEnum(str, Enum):
    ASSENTO = "assento"
    PRODUTO = "produto"

class StatusSessaoEnum(str, Enum):
    ATIVA = "ativa"
    ENCERRADA = "encerrada"
    CANCELADA = "cancelada"

class StatusSalaEnum(str, Enum):
    ATIVA = "ativo"
    MANUTENCAO = "em_manutencao"
    INATIVO = "inativo"

class StatusAssentoEnum(str, Enum):
    DISPONIVEL = "disponivel"
    RESERVADO = "reservado"
    OCUPADO = "ocupado"
    INDISPONIVEL = "indisponivel"