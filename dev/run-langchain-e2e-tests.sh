#!/bin/bash
set -e

check_env() {
  local var_name=$1
  if [ -z "${!var_name}" ]; then
      echo "Error: Environment variable '$var_name' is missing."
      #exit 1
  fi
}

# astra
check_env ASTRA_DB_TOKEN
check_env ASTRA_DB_ENDPOINT

export ASTRA_DB_APPLICATION_TOKEN=$ASTRA_DB_TOKEN
export ASTRA_DB_API_ENDPOINT=$ASTRA_DB_ENDPOINT


cd ragstack-langchain/libs/langchain
poetry install --with test,test_integration
poetry run pytest tests/integration_tests/vectorstores/test_astradb.py