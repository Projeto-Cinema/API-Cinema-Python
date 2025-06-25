# --- Makefile para o Projeto de API de Cinema ---

# Define que os alvos não são nomes de arquivos, evitando conflitos.
.PHONY: help lint format build up down logs

# O alvo padrão, executado se você apenas digitar "make"
help:
	@echo "Comandos disponíveis:"
	@echo "  make help          - Mostra esta mensagem de ajuda."
	@echo "  make lint          - Roda as verificações de Flake8, Black e iSort no código."
	@echo "  make format        - Formata o código automaticamente com Black e iSort."
	@echo "  make build         - Constrói ou reconstrói as imagens Docker."
	@echo "  make up            - Sobe os contêineres Docker em modo detached."
	@echo "  make down          - Para e remove os contêineres Docker."
	@echo "  make logs          - Mostra os logs do contêiner da API."

# Alvo para rodar as verificações de qualidade (lint)
lint:
	@echo "▶️  Executando verificações de qualidade..."
	@./scripts/lint.sh app

# Alvo para formatar o código automaticamente
format:
	@echo "▶️  Formatando o código..."
	@pre-commit run black --files app/*
	@pre-commit run isort --files app/*

# Alvos para gerenciamento do Docker
build:
	@echo "▶️  Construindo imagens Docker..."
	@docker-compose build

up:
	@echo "▶️  Subindo ambiente Docker..."
	@docker-compose up -d

down:
	@echo "▶️  Parando ambiente Docker..."
	@docker-compose down

logs:
	@echo "▶️  Mostrando logs da API..."
	@docker-compose logs -f api
