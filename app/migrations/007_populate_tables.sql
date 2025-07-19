INSERT INTO public.usuario (nome, email, senha, dt_nascimento, cpf, telefone, ativo, tipo, ultimo_acesso) VALUES 
('admin','admin@gmail.com','$2a$12$VsZzKFT7ZzxZG6wLteHwEuImpc2plyVz.2Cdk9a7RnoVFuurFYe.C',NULL,'12345678998',NULL,TRUE,'admin',NULL),
('cliente','cliente@gmail.com','$2a$12$n74xpn7fysrLc7BXksjdd.GS5X7AScNpr2MycyybxIi..Eg4veRzC',NULL,'14725836998',NULL,TRUE,'cliente',NULL);

INSERT INTO public.endereco (cep, logradouro, numero, complemento, bairro, cidade, estado, referencia) VALUES
('01311-000', 'Avenida Paulista', '1578', 'Andar 10', 'Bela Vista', 'São Paulo', 'SP', 'Próximo ao MASP');

INSERT INTO public.cinema (endereco_id, nome, cnpj, email, site, horario_func) VALUES
(1, 'Cine Estrela Paulista', '11.111.111/0001-11', 'contato@estrela-sp.com', 'http://www.estrela-sp.com', '13:00-23:00');

INSERT INTO public.filme (titulo, titulo_original, sinopse, duracao_min, diretor, elenco, classificacao, ano_lancamento, em_cartaz) VALUES
('As Crônicas de Zylos', 'The Chronicles of Zylos', 'Em um mundo distante, um herói improvável deve encontrar a lendária Espada de Luz para derrotar o tirano das sombras.', 145, 'J. J. Abrams', 'Ana de Armas, Chris Evans, Samuel L. Jackson', '12 anos', 2023, TRUE),
('O Último Robô da Terra', 'The Last Robot on Earth', 'Após um evento cataclísmico, um robô de manutenção solitário descobre que pode não estar sozinho no planeta.', 98, 'Denis Villeneuve', 'Voz de Tom Hanks', 'Livre', 2024, TRUE),
('Amor em Paris', 'Love in Paris', 'Uma chef de cozinha e um crítico de arte se encontram em Paris e vivem uma história de amor cheia de reviravoltas e croissants.', 110, 'Greta Gerwig', 'Florence Pugh, Timothée Chalamet', '10 anos', 2022, FALSE),
('Agente Secreto 7', 'Secret Agent 7', 'O melhor espião do mundo precisa impedir uma organização criminosa de lançar uma arma cibernética global.', 130, 'Christopher Nolan', 'Idris Elba, Margot Robbie, Cillian Murphy', '14 anos', 2024, TRUE),
('A Viagem da Família Pinguim', 'The Penguin Family Trip', 'Uma adorável família de pinguins se perde durante sua migração anual e precisa encontrar o caminho de volta para casa.', 85, 'Pixar Studios', 'Vozes de John Krasinski, Emily Blunt', 'Livre', 2023, TRUE);

INSERT INTO public.filme_genero (filme_id, genero_id) VALUES
(1, 3), -- As Crônicas de Zylos -> Comédia
(2, 3), -- O Último Robô da Terra -> Comédia
(2, 4), -- O Último Robô da Terra -> Drama
(3, 2), -- Amor em Paris -> Aventura
(4, 1), -- Agente Secreto 7 -> Ação
(5, 5), -- A Viagem da Família Pinguim -> Fantasia
(5, 2); -- A Viagem da Família Pinguim -> Aventura

INSERT INTO public.sala (cinema_id, nome, capacidade, tipo, recursos, status) VALUES
(1, 'Sala 1', 150, 'IMAX', 'Som Dolby Atmos, Tela Gigante', 'ativo'),
(1, 'Sala 2', 100, 'Comum', 'Som Digital 7.1', 'ativo'),
(1, 'Sala 3 VIP', 50, 'VIP', 'Poltronas reclináveis, Serviço de bar', 'ativo'),
(1, 'Sala 4 Cult', 80, 'De Arte', 'Projetor 35mm', 'em_manutencao'),
(1, 'Sala 5 3D', 120, '3D', 'Óculos 3D ativos', 'ativo');

INSERT INTO public.assento_sala (sala_id, codigo, tipo, posicao_x, posicao_y) VALUES
(1, 'A1', 'comum', 1, 1), (1, 'A2', 'comum', 1, 2), (1, 'B1', 'comum', 2, 1), (1, 'B2', 'comum', 2, 2),
-- Sala 2 (ID 2)
(2, 'C5', 'comum', 3, 5), (2, 'C6', 'comum', 3, 6), (2, 'D5', 'premium', 4, 5), (2, 'D6', 'premium', 4, 6),
-- Sala 3 (ID 3)
(3, 'V1', 'vip', 1, 1), (3, 'V2', 'vip', 1, 2), (3, 'V3', 'casal', 1, 3),
-- Sala 5 (ID 5)
(5, 'E10', 'comum', 5, 10), (5, 'E11', 'comum', 5, 11), (5, 'F10', 'comum', 6, 10), (5, 'F11', 'comum', 6, 11);

INSERT INTO public.sessao (filme_id, sala_id, data, horario_ini, horario_fim, idioma, legendado, formato, preco_base) VALUES
(1, 1, CURRENT_DATE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + interval '2 hours 30 minutes', 'Inglês', TRUE, 'IMAX', 50.00),
(2, 5, CURRENT_DATE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + interval '1 hour 45 minutes', 'Inglês', TRUE, '3D', 45.00),
(4, 3, CURRENT_DATE, CURRENT_TIMESTAMP + interval '1 day', CURRENT_TIMESTAMP + interval '1 day' + interval '2 hours 15 minutes', 'Inglês', TRUE, '2D VIP', 70.00),
(5, 2, CURRENT_DATE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + interval '1 hour 30 minutes', 'Português', FALSE, '2D', 30.00),
(1, 2, CURRENT_DATE, CURRENT_TIMESTAMP + interval '3 hours', CURRENT_TIMESTAMP + interval '5 hours 30 minutes', 'Português', FALSE, '2D', 35.00);

INSERT INTO public.produto (cinema_id, nome, descricao, categoria, preco, imagem_url) VALUES
(1, 'Pipoca Grande Salgada', 'Pipoca estourada na hora com manteiga opcional.', 'Pipoca', 25.00, 'http://example.com/pipoca.jpg'),
(1, 'Refrigerante 700ml', 'Coca-Cola, Guaraná ou Fanta.', 'Bebidas', 15.00, 'http://example.com/refri.jpg'),
(1, 'Combo Casal', '2 Pipocas Médias + 2 Refrigerantes 500ml.', 'Combos', 65.00, 'http://example.com/combo.jpg'),
(1, 'Chocolate M&Ms', 'Pacote de M&Ms 100g.', 'Doces', 12.00, 'http://example.com/mms.jpg'),
(1, 'Água Mineral', 'Garrafa de 500ml sem gás.', 'Bebidas', 8.00, NULL);
