INSERT INTO public.genero (nome) VALUES
    ('Ação'),
    ('Aventura'),
    ('Comédia'),
    ('Drama'),
    ('Fantasia'),
    ('Ficção Científica'),
    ('Terror'),
    ('Romance'),
    ('Animação'),
    ('Documentário'),
    ('Musical'),
    ('Suspense'),
    ('Policial'),
    ('Guerra'),
    ('Histórico')
ON CONFLICT (nome) DO NOTHING;