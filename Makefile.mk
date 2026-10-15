.PHONY: help install test verify run clean docker-test docker-verify docker-run

PYTHON ?= python3
VENV   ?= .venv
BIN    := $(VENV)/bin
OUT    ?= output

help:
	@echo "gargalo-lab — comandos disponíveis:"
	@echo "  make install        cria venv e instala dependências (editable)"
	@echo "  make test           roda os 17 testes (unittest)"
	@echo "  make verify         confere os 16 resultados de referência do artigo"
	@echo "  make run            roda os 8 labs (saída em ./$(OUT))"
	@echo "  make clean          remove venv, caches e saída"
	@echo "  make docker-test    roda os testes via docker compose"
	@echo "  make docker-verify  roda a verificação via docker compose"
	@echo "  make docker-run     roda os 8 labs via docker compose"

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e .
	@echo "✓ Ambiente pronto. Ative com: source $(BIN)/activate"

test:
	PYTHONPATH=. $(BIN)/python -m unittest discover -s tests -v

verify:
	PYTHONPATH=. $(BIN)/python -m gargalo_lab verify --out $(OUT)

run:
	PYTHONPATH=. $(BIN)/python -m gargalo_lab all --out $(OUT)

clean:
	rm -rf $(VENV) $(OUT) .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

docker-test:
	docker compose run --rm --build tests

docker-verify:
	docker compose run --rm --build verify

docker-run:
	docker compose up --build lab