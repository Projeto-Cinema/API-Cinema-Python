# Testes da aplicação FastAPI

Este diretório contém os testes unitários e de integração para a aplicação FastAPI.

## Estrutura de testes

- `conftest.py`: Configurações globais e fixtures para os testes
- `test_main.py`: Testes dos endpoints da API
- `test_models.py`: Testes dos modelos de dados

## Executando os testes

### Localmente

```bash
# Instalar dependências de teste
pip install -r test_requirements.txt

# Executar todos os testes
pytest

# Executar testes com coverage
pytest --cov=.

# Executar um arquivo específico
pytest tests/test_main.py

# Executar um teste específico
pytest tests/test_main.py::test_read_root
```

### Usando Docker

```bash
# Construir e executar os testes no Docker
docker-compose build tests
docker-compose run tests

# Executar com opções específicas
docker-compose run tests pytest tests/test_main.py -v
```

## Marcadores de testes

Alguns testes estão marcados com `@pytest.mark.skip` porque as funcionalidades correspondentes ainda não foram implementadas. Quando implementar essas funcionalidades, remova os marcadores para ativar os testes.

## Cobertura de testes

Os testes foram configurados para gerar relatórios de cobertura usando pytest-cov. Para ver um relatório detalhado:

```bash
docker-compose run tests pytest --cov=. --cov-report=html
```

Isso gerará um diretório `htmlcov` com o relatório completo de cobertura.