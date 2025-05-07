#!/bin/bash

# Script para executar os testes do projeto

# Certificar-se de que o arquivo seja executável
# chmod +x run_tests.sh

# Opções padrão
DOCKER=true
COVERAGE=false
TEST_PATH="tests"
VERBOSE=false

# Função de ajuda
function show_help {
  echo "Uso: ./run_tests.sh [opções]"
  echo ""
  echo "Opções:"
  echo "  -h, --help          Mostra esta mensagem de ajuda"
  echo "  -l, --local         Executa testes localmente (sem Docker)"
  echo "  -c, --coverage      Gera relatório de cobertura de código"
  echo "  -p, --path PATH     Especifica caminho/arquivo de teste específico"
  echo "  -v, --verbose       Executa testes com saída detalhada"
  echo ""
  echo "Exemplos:"
  echo "  ./run_tests.sh                     # Executa todos os testes no Docker"
  echo "  ./run_tests.sh -l -c               # Executa localmente com cobertura"
  echo "  ./run_tests.sh -p tests/test_main.py  # Testa apenas test_main.py"
}

# Processar argumentos
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      exit 0
      ;;
    -l|--local)
      DOCKER=false
      shift
      ;;
    -c|--coverage)
      COVERAGE=true
      shift
      ;;
    -p|--path)
      TEST_PATH="$2"
      shift
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    *)
      echo "Opção desconhecida: $1"
      show_help
      exit 1
      ;;
  esac
done

# Construir comando de teste
PYTEST_CMD="pytest $TEST_PATH"

if [ "$COVERAGE" = true ]; then
  PYTEST_CMD="$PYTEST_CMD --cov=. --cov-report=term"
fi

if [ "$VERBOSE" = true ]; then
  PYTEST_CMD="$PYTEST_CMD -v"
fi

# Executar testes
if [ "$DOCKER" = true ]; then
  echo "Executando testes no Docker: $PYTEST_CMD"
  docker-compose build tests
  docker-compose run tests $PYTEST_CMD
else
  echo "Executando testes localmente: $PYTEST_CMD"
  $PYTEST_CMD
fi

# Exibir resultado
if [ $? -eq 0 ]; then
  echo "✅ Testes concluídos com sucesso!"
else
  echo "❌ Falha nos testes!"
  exit 1
fi