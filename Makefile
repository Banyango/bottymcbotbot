# Makefile to run ruff and pyright (prefers uv if available)
RUN := export PYTHONPATH=src && uv run

.PHONY: lint typecheck check install-dev

format:
	$(RUN) ruff format

lint:
	$(RUN) ruff check . --fix
	$(RUN) pyright src tests

check: lint typecheck

install-dev:
ifeq ($(UV),)
	@echo "uv not found; please install ruff and pyright in your PATH or install uv."
else
	uv install --with dev
endif

create-migration:
	$(RUN) alembic revision --autogenerate -m "$(msg)"

apply-migrations:
	$(RUN) alembic upgrade head

down-migrations:
	$(RUN) alembic downgrade -1
