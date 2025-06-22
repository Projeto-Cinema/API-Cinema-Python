INSERT INTO public.assento_sala (sala_id, codigo, tipo, posicao_x, posicao_y) VALUES
-- Fileira A (frente) - assentos comuns
(1, 'A1', 'comum', 1, 1), (1, 'A2', 'comum', 2, 1), (1, 'A3', 'comum', 3, 1), (1, 'A4', 'comum', 4, 1), (1, 'A5', 'comum', 5, 1),
(1, 'A6', 'comum', 6, 1), (1, 'A7', 'comum', 7, 1), (1, 'A8', 'comum', 8, 1), (1, 'A9', 'comum', 9, 1), (1, 'A10', 'comum', 10, 1),

-- Fileira B - assentos comuns
(1, 'B1', 'comum', 1, 2), (1, 'B2', 'comum', 2, 2), (1, 'B3', 'comum', 3, 2), (1, 'B4', 'comum', 4, 2), (1, 'B5', 'comum', 5, 2),
(1, 'B6', 'comum', 6, 2), (1, 'B7', 'comum', 7, 2), (1, 'B8', 'comum', 8, 2), (1, 'B9', 'comum', 9, 2), (1, 'B10', 'comum', 10, 2),

-- Fileira C - assentos comuns
(1, 'C1', 'comum', 1, 3), (1, 'C2', 'comum', 2, 3), (1, 'C3', 'comum', 3, 3), (1, 'C4', 'comum', 4, 3), (1, 'C5', 'comum', 5, 3),
(1, 'C6', 'comum', 6, 3), (1, 'C7', 'comum', 7, 3), (1, 'C8', 'comum', 8, 3), (1, 'C9', 'comum', 9, 3), (1, 'C10', 'comum', 10, 3),

-- Fileira D - assentos VIP (meio da sala)
(1, 'D1', 'vip', 1, 4), (1, 'D2', 'vip', 2, 4), (1, 'D3', 'vip', 3, 4), (1, 'D4', 'vip', 4, 4), (1, 'D5', 'vip', 5, 4),
(1, 'D6', 'vip', 6, 4), (1, 'D7', 'vip', 7, 4), (1, 'D8', 'vip', 8, 4), (1, 'D9', 'vip', 9, 4), (1, 'D10', 'vip', 10, 4),

-- Fileira E (fundo) - assentos casal
(1, 'E1', 'casal', 1, 5), (1, 'E2', 'casal', 3, 5), (1, 'E3', 'casal', 5, 5), (1, 'E4', 'casal', 7, 5), (1, 'E5', 'casal', 9, 5);

-- Exemplo para sala média (ID 2) - Layout mais complexo
-- 80 assentos: fileiras A-F, com corredores

INSERT INTO public.assento_sala (sala_id, codigo, tipo, posicao_x, posicao_y) VALUES
-- Fileira A - 12 assentos comuns
(2, 'A1', 'comum', 1, 1), (2, 'A2', 'comum', 2, 1), (2, 'A3', 'comum', 3, 1), (2, 'A4', 'comum', 4, 1),
-- corredor --
(2, 'A5', 'comum', 6, 1), (2, 'A6', 'comum', 7, 1), (2, 'A7', 'comum', 8, 1), (2, 'A8', 'comum', 9, 1),
-- corredor --
(2, 'A9', 'comum', 11, 1), (2, 'A10', 'comum', 12, 1), (2, 'A11', 'comum', 13, 1), (2, 'A12', 'comum', 14, 1),

-- Fileira B - 12 assentos comuns
(2, 'B1', 'comum', 1, 2), (2, 'B2', 'comum', 2, 2), (2, 'B3', 'comum', 3, 2), (2, 'B4', 'comum', 4, 2),
(2, 'B5', 'comum', 6, 2), (2, 'B6', 'comum', 7, 2), (2, 'B7', 'comum', 8, 2), (2, 'B8', 'comum', 9, 2),
(2, 'B9', 'comum', 11, 2), (2, 'B10', 'comum', 12, 2), (2, 'B11', 'comum', 13, 2), (2, 'B12', 'comum', 14, 2),

-- Fileira C - 12 assentos VIP
(2, 'C1', 'vip', 1, 3), (2, 'C2', 'vip', 2, 3), (2, 'C3', 'vip', 3, 3), (2, 'C4', 'vip', 4, 3),
(2, 'C5', 'vip', 6, 3), (2, 'C6', 'vip', 7, 3), (2, 'C7', 'vip', 8, 3), (2, 'C8', 'vip', 9, 3),
(2, 'C9', 'vip', 11, 3), (2, 'C10', 'vip', 12, 3), (2, 'C11', 'vip', 13, 3), (2, 'C12', 'vip', 14, 3),

-- Fileira D - 12 assentos premium
(2, 'D1', 'premium', 1, 4), (2, 'D2', 'premium', 2, 4), (2, 'D3', 'premium', 3, 4), (2, 'D4', 'premium', 4, 4),
(2, 'D5', 'premium', 6, 4), (2, 'D6', 'premium', 7, 4), (2, 'D7', 'premium', 8, 4), (2, 'D8', 'premium', 9, 4),
(2, 'D9', 'premium', 11, 4), (2, 'D10', 'premium', 12, 4), (2, 'D11', 'premium', 13, 4), (2, 'D12', 'premium', 14, 4),

-- Fileira E - 6 assentos casal
(2, 'E1', 'casal', 2, 5), (2, 'E2', 'casal', 4, 5), (2, 'E3', 'casal', 7, 5), (2, 'E4', 'casal', 9, 5), (2, 'E5', 'casal', 12, 5), (2, 'E6', 'casal', 14, 5);

-- Script para gerar assentos automaticamente para outras salas
-- (Você pode adaptar conforme necessário)

-- Função auxiliar para criar layout padrão
CREATE OR REPLACE FUNCTION criar_assentos_padrao(
    p_sala_id INTEGER,
    p_fileiras INTEGER DEFAULT 5,
    p_assentos_por_fileira INTEGER DEFAULT 10
) RETURNS VOID AS $$
DECLARE
    fileira_char CHAR(1);
    i INTEGER;
    j INTEGER;
    tipo_assento VARCHAR(20);
BEGIN
    FOR i IN 1..p_fileiras LOOP
        fileira_char := CHR(64 + i); -- A, B, C, D, E...
        
        FOR j IN 1..p_assentos_por_fileira LOOP
            -- Definir tipo baseado na fileira
            CASE 
                WHEN i <= 2 THEN tipo_assento := 'comum';
                WHEN i = 3 THEN tipo_assento := 'vip';
                WHEN i = 4 THEN tipo_assento := 'premium';
                ELSE tipo_assento := 'casal';
            END CASE;
            
            INSERT INTO public.assento_sala (sala_id, codigo, tipo, posicao_x, posicao_y)
            VALUES (p_sala_id, fileira_char || j::TEXT, tipo_assento, j, i);
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;