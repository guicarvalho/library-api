clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

install:
	uv sync

init-modules:
	find app tests -type d -exec touch {}/__init__.py \;

lint:
	uv run ruff check .

format:
	uv run ruff format .

serve:
	uv run fastapi dev app/main.py --port 8000

test-unit:
	uv run pytest tests/unit

test-integration:
	uv run pytest tests/integration

test:
	make test-unit && make test-integration

db-makemigration:
	uv run alembic revision --autogenerate

db-upgrade:
	uv run alembic upgrade head

db-rollback:
	uv run alembic downgrade -1
