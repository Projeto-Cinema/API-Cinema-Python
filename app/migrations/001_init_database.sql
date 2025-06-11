-- Tabela Endereco

CREATE TABLE IF NOT EXISTS public.endereco (
    id SERIAL,
    cep VARCHAR(10) NOT NULL,
    logradouro VARCHAR(255) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    complemento VARCHAR(100) NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NULL,
    referencia VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT endereco_pk PRIMARY KEY (id)
);

-- Tabela Usuario

CREATE TABLE IF NOT EXISTS public.usuario (
    id SERIAL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    dt_nascimento TIMESTAMP NULL,
    cpf VARCHAR(14) NOT NULL,
    telefone VARCHAR(20) NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    dt_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo VARCHAR(20) NOT NULL DEFAULT 'cliente',
    ultimo_acesso TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT usuario_pk PRIMARY KEY (cpf)
);

-- Tabela CINEMA

CREATE TABLE IF NOT EXISTS public.cinema (
    id SERIAL,
    endereco_id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(20) NOT NULL UNIQUE,
    telefone VARCHAR(20) NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    site VARCHAR(255) NULL,
    horario_func VARCHAR(50) NULL,
    imagem_url VARCHAR(255) NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT cinema_pk PRIMARY KEY (id),
    CONSTRAINT cinema_endereco_fk FOREIGN KEY (endereco_id)
        REFERENCES public.endereco (id) ON DELETE RESTRICT
);

-- TABELA PRODUTO

CREATE TABLE IF NOT EXISTS public.produto (
    id SERIAL,
    cinema_id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    imagme_url VARCHAR(255) NULL,
    disponivel BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT produto_pk PRIMARY KEY (id),
    CONSTRAINT produto_cinema_fk FOREIGN KEY (cinema_id)
        REFERENCES public.cinema (id) ON DELETE CASCADE
);

-- TABELA SALA

CREATE TABLE IF NOT EXISTS public.sala (
    id SERIAL,
    cinema_id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    capacidade INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    recursos VARCHAR(255) NULL,
    mapa_assentos TEXT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'disponivel',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT sala_pk PRIMARY KEY (id),
    CONSTRAINT sala_cinema_fk FOREIGN KEY (cinema_id)
        REFERENCES public.cinema (id) ON DELETE CASCADE,

    CONSTRAINT sala_capacidade_check CHECK (capacidade > 0),
    CONSTRAINT sala_status_check CHECK (status IN ('ativo', 'em_manutencao', 'inativo'))
);

-- TABELA FILME

CREATE TABLE IF NOT EXISTS public.filme (
    id SERIAL,
    titulo VARHCAR(100) NOT NULL,
    titulo_original VARCHAR(100) NOT NULL,
    sinopse TEXT NOT NULL,
    duracao_min INTEGER NOT NULL,
    diretor VARCHAR(100) NOT NULL,
    elenco TEXT NOT NULL,
    generos TEXT NOT NULL,
    classificacao VARCHAR(10) NOT NULL,
    ano_lancamento INTEGER NOT NULL,
    em_cartaz BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT filme_pk PRIMARY KEY (id),

    CONSTRAINT filme_duracao_check CHECK (duracao_min > 0),
    CONSTRAINT 
        filme_ano_check 
    CHECK 
        (
            ano_lancamento > 1800 AND 
            ano_lacamento <= EXTRACT(YEAR FROM CURRENT_DATE) + 5
        )
);

-- TABELA SESSAO

CREATE TABLE IF NOT EXISTS public.sessao (
    id SERIAL,
    filme_id INTEGER NOT NULL,
    sala_id INTEGER NOT NULL,
    data DATE NOT NULL,
    horario_ini TIMESTAMP NOT NULL,
    horario_fim TIMESTAMP NOT NULL,
    idioma VARCHAR(20) NOT NULL,
    legendado BOOLEAN NOT NULL DEFAULT FALSE,
    formato VARCHAR(20) NOT NULL,
    preco_base DECIMAL(8,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ativa',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT sessao_pk PRIMARY KEY (id),
    CONSTRAINT sessao_filme_fk FOREIGN KEY (filme_id)
        REFERENCES public.filme (id) ON DELETE CASCADE,
    CONSTRAINT sessao_sala_fk FOREIGN KEY (sala_id)
        REFERENCES public.sala (id) ON DELETE CASCADE,

    CONSTRAINT sessao_horario_check CHECK (horario_fim > horario_ini),
    CONSTRAINT sessao_preco_check CHECK (preco_base >= 0),
    CONSTRAINT sessao_status_check CHECK (status IN ('ativa', 'cancelada', 'encerrada'))
);

-- TABELA ASSENTO

CREATE TABLE IF NOT EXISTS public.assento (
    id SERIAL,
    sessao_id INTEGER NOT NULL,
    codigo VARCHAR(10) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    preco DECIMAL(8,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'disponivel',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT assento_pk PRIMARY KEY (id),
    CONSTRAINT assento_sessao_fk FOREIGN KEY (sessao_id)
        REFERENCES public.sessao (id) ON DELETE CASCADE,

    CONSTRAINT assento_preco_check CHECK (preco >= 0),
    CONSTRAINT assento_status_check CHECK (status IN ('disponivel', 'reservado', 'ocupado', 'indisponivel')),

    CONSTRAINT assento_sessao_codigo_uk UNIQUE (sessao_id, codigo)
);

-- TABELA RESERVA

CREATE TABLE IF NOT EXISTS public.reserva (
    id SERIAL,
    usuario_id INTEGER NOT NULL,
    sessao_id INTEGER NOT NULL,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    data_reserva TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',
    valor_total DECIMAL(10,2) NOT NULL,
    metodo_pagamento VARCHAR(50) NOT NULL,
    assentos TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT reserva_pk PRIMARY KEY (id),
    CONSTRAINT reserva_usuario_fk FOREIGN KEY (usuario_id)
        REFERENCES public.usuario (id) ON DELETE CASCADE,
    CONSTRAINT reserva_sessao_fk FOREIGN KEY (sessao_id)
        REFERENCES public.sessao (id) ON DELETE CASCADE,

    CONSTRAINT reserva_valor_check CHECK (valor_total >= 0),
    CONSTRAINT reserva_status_check CHECK (status IN ('pendente', 'confirmado', 'cancelada', 'expirado'))
);

-- TABELA ITEM_RESERVA

CREATE TABLE IF NOT EXISTS public.item_reserva (
    id SERIAL,
    reserva_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(10,2) NOT NULL,
    preco_total DECIMAL(10,2) NOT NULL,
    desconto DECIMAL(8,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT item_reserva_pk PRIMARY KEY (id),

    CONSTRAINT item_reserva_reserva_fk FOREIGN KEY (reserva_id)
        REFERENCES public.reserva (id) ON DELETE CASCADE,

    CONSTRAINT item_reserva_quantidade_check CHECK (quantidade > 0),
    CONSTRAINT item_reserva_preco_unitario_check CHECK (preco_unitario >= 0),
    CONSTRAINT item_reserva_preco_total_check CHECK (preco_total >= 0),
    CONSTRAINT item_reserva_desconto_check CHECK (desconto >= 0),
    CONSTRAINT item_reserva_tipo_check CHECK (tipo IN ('assento', 'produto'))
);

-- TABELA PAGAMENTO

CREATE TABLE IF NOT EXISTS public.pagamento (
    id SERIAL,
    reserva_id INTEGER NOT NULL UNIQUE,
    valor DECIMAL(10,2) NOT NULL,
    metodo VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',
    dt_pagamento TIMESTAMP NULL,
    referencia_externa VARCHAR(100) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pagamento_pk PRIMARY KEY (id),
    CONSTRAINT pagamento_reserva_fk FOREIGN KEY (reserva_id)
        REFERENCES public.reserva (id) ON DELETE CASCADE,

    CONSTRAINT pagamento_valor_check CHECK (valor >= 0),
    CONSTRAINT pagamento_status_check CHECK (status IN ('pendente', 'aprovado', 'recusado', 'reembolsado'))
);