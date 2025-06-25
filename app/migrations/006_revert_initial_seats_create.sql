DELETE FROM public.assento_sala
WHERE sala_id IN (1, 2);

DROP FUNCTION IF EXISTS criar_assentos_padrao(INTEGER, INTEGER, INTEGER);
