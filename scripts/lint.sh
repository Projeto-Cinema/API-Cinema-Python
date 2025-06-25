#!/bin/bash

# --- Script para executar verificações de qualidade de código ---
# Este script para imediatamente se qualquer comando falhar (set -e).
set -e

# O diretório alvo para a verificação, passado como primeiro argumento.
# Se nenhum for passado, usa 'app' como padrão.
TARGET_DIR=${1:-app}

echo "✅ Executando verificações de qualidade no diretório: $TARGET_DIR"
echo "-----------------------------------------------------"

# 1. Executa o Flake8 para encontrar erros de lógica e estilo.
echo "🔎 Rodando o Flake8..."
pre-commit run flake8 --files $TARGET_DIR/*

# 2. Executa o Black em modo --check para verificar a formatação.
echo "🎨 Verificando a formatação com o Black..."
pre-commit run black --files $TARGET_DIR/*

# 3. Executa o iSort em modo --check para verificar a ordem dos imports.
echo "📦 Verificando a ordem dos imports com o iSort..."
pre-commit run isort --files $TARGET_DIR/*

echo "-----------------------------------------------------"
echo "🎉 Todas as verificações passaram com sucesso!"
