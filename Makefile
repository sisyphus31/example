NAME := example
INSTALL_STAMP := .install.stamp
UV := $(shell command -v uv 2> /dev/null)

export UV_LINK_MODE := copy

.DEFAULT_GOAL := help

# WTF man: https://github.com/astral-sh/uv/issues/1327 - Guard against deletion of the current environment 

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  clean       remove all temporary files"
	@echo "  lint        run the code linters"
	@echo "  format      reformat code"
	@echo "  test        run all the tests"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml
	@if [ -z $(UV) ]; then echo "uv could not be found. See https://docs.astral.sh/uv/getting-started/installation/"; exit 2; fi
	$(UV) venv
	$(UV) pip compile pyproject.toml --all-extras
	touch $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) .coverage .mypy_cache .venv

.PHONY: lint
lint: $(INSTALL_STAMP)
	$(UV) run --env-file .env ruff format --check --diff .
	$(UV) run --env-file .env ruff check .
	$(UV) run --env-file .env mypy src/$(NAME) --strict

.PHONY: format
format: $(INSTALL_STAMP)
	$(UV) run --env-file .env ruff format .
	$(UV) run --env-file .env ruff check --show-fixes --fix-only .

.PHONY: test
test: $(INSTALL_STAMP)
	$(UV) run pytest ./src/tests/
