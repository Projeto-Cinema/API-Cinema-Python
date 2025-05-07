# API FastAPI com PostgreSQL

Esse projeto tem com intuito refazer um antigo projeto acadêmico, da matéria Orientação de Objetos na FCTE/UnB, em que antes foi escrito em Java e usando Java Swing porém agora foi reescrito para Python e implementado para ser uma API. Este projeto foi desenvolvido durante a matéria de Técnicas de Programação em Plataformas Emergentes do Professor Thiago.

Abaixo deixarei os links úteis em relação ao projeto:
- [Trabalho de Orientação Objeto - Java](https://github.com/Weslin-0101/TP2)
- [Trello](https://trello.com/invite/b/681b44a49d2f271ba466f084/ATTIc161d83860e180a18250a5d979ba2c9991879A13/api-cinema)
- [Diagrama de Classes](https://lucid.app/lucidchart/fa2d7236-980f-451d-875f-54139fed556f/edit?viewport_loc=-3297%2C-1802%2C4764%2C2577%2C0_0&invitationId=inv_bf9d3fbb-3b20-403b-841c-67323ebee7ac)

## Requisitos
- Docker
- Docker Compose
- GIT

## Iniciando o Projeto

1) Clone este repositório por meio deste comando abaixo:
```
    git clone https://github.com/Weslin-0101/TP2.git
```
2) Execute os containers com os seguintes comandos:

```bash
    docker-compoe up --build -d
```
3) A API estará disponível em: http://localhost:8000

## Executando Testes

Para executar os testes do projeto siga os seguintes passos.

Execute os testes pelo arquivo:
```bash
# Tornar o scrip executável
chmod +x run_tests.sh

# Executar todos os testes
./run_tests.sh

# Ver todas as opções disponívels para executar o teste
./run_tests.sh --help
```

Ou mesmo pode executar diretamente utilizando o docker-compose:
```bash
docker-compose run tests
```

## Configuração do Banco de Dados

O banco de dados que está sendo utilizado é o PostgreSQL. A configuração dele é a seguinte:
- **Host**: db
- **Porta**: 5432
- **user**: postgres
- **password**: postgres
- **database**: fastapi_db

## Desenvolvimento:

Para trabalhar com o projeto localmente, faça:

1) Crie um ambiente virtualizado:
```bash
    python -m venv venv
    source venv/bin/activate # Para Linux/Mac
    venv/Scripts/activate # Para Windows
```

2) Instale as dependências:
```bash
    pip install -r requirements.txt
    pip install -r test_requirements.txt
```

3) Execute a aplicação:
```bash
    uvicorn main:app --reload
```