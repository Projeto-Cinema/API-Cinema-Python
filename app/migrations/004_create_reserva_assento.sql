ALTER TABLE public.reserva
    DROP COLUMN IF EXISTS assentos;

ALTER TABLE public.reserva
    ALTER COLUMN metodo_pagamento DROP NOT NULL;

UPDATE public.reserva SET status = 'confirmado' WHERE status = 'confirmado';
UPDATE public.reserva SET status = 'expirada' WHERE status = 'expirado';

ALTER TABLE public.reserva
    DROP CONSTRAINT IF EXISTS reserva_status_check;

ALTER TABLE public.reserva
    ADD CONSTRAINT reserva_status_check CHECK (status IN ('pendente', 'confirmada', 'cancelada', 'expirada'));

ALTER TABLE public.assento_sala
    ADD COLUMN IF NOT EXISTS preco_adicional DECIMAL(8, 2) NOT NULL DEFAULT 0.0;

DROP TABLE IF EXISTS public.reserva_assento;

DROP TABLE IF EXISTS public.assento;