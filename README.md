# RAGStack

## Clone this Repository

This repository includes `ragstack-langchain` and `ragstack-langsmith` as Git submodules. To clone these submodules along with the main repository, you can use one of the following methods:

Clone Recursively: This method allows you to clone the main repository and its submodules in a single command.

```shell
git clone --recurse-submodules git@github.com:datastax/ragstack-ai.git
```

Initialize Submodules After Cloning: If you have already cloned the main repository and now need to include the submodules, you can initialize and update them with the following commands:

```shell
git submodule init
git submodule update
```

## Poetry set up

The project uses [poetry](https://python-poetry.org/).
To install poetry:

```shell
pip install poetry
```

## Install dependencies
```shell
poetry install
```

## Run Tests

```shell
poetry run pytest tests/unit-tests
```

## Run End-to-End tests
End-to-end testing requires a lot of external service credentials.
The required environment variables that need to be set for the tests to run successfully can be found in the [tox.ini](./ragstack-e2e-tests/tox.ini).

```shell
poetry run tox -c ragstack-e2e-tests
```

## Build the package distribution
```shell
poetry build
```
