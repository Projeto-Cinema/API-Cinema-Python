CREATE TABLE IF NOT EXISTS public.assento_sala (
    id SERIAL,
    sala_id INTEGER NOT NULL,
    codigo VARCHAR(10) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    posicao_x INTEGER NOT NULL,
    posicao_y INTEGER NOT NULL,
    ativo VARCHAR(20) NOT NULL DEFAULT 'ativo',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT assento_sala_pk PRIMARY KEY (id),
    CONSTRAINT assento_sala_sala_fk FOREIGN KEY (sala_id)
        REFERENCES public.sala (id) ON DELETE CASCADE,

    CONSTRAINT assento_sala_ativo_check CHECK (ativo IN ('ativo', 'inativo', 'manutencao')),
    CONSTRAINT assento_sala_tipo_check CHECK (tipo IN ('normal', 'vip', 'casal', 'premium')),

    CONSTRAINT assento_sala_codigo_uk UNIQUE (sala_id, codigo) 
);

CREATE TABLE IF NOT EXISTS public.assento_bakcup AS
    SELECT * FROM public.assento;

ALTER TABLE public.assento
    ADD COLUMN IF NOT EXISTS assento_sala_id INTEGER;

ALTER TABLE public.assento
    DROP COLUMN IF EXISTS codigo,
    DROP COLUMN IF EXISTS tipo;

ALTER TABLE public.assento
    ADD CONSTRAINT assento_assento_sala_fk FOREIGN KEY (assento_sala_id)
        REFERENCES public.assento_sala (id) ON DELETE CASCADE;

ALTER TABLE public.assento
    DROP CONSTRAINT IF EXISTS assento_sessao_codigo_uk;

ALTER TABLE public.assento
    ADD CONSTRAINT assento_sessao_sala_uk UNIQUE (sessao_id, assento_sala_id);