FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN pip install --upgrade uv

COPY pyproject.toml uv.lock ./

RUN uv venv && uv sync --no-dev --frozen

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

WORKDIR /app

RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv .venv
COPY --from=builder /app/uv.lock /app/pyproject.toml ./

COPY src ./src

# TODO: create Docker image specifies to run migrations in the database
COPY infrastructure/alembic ./infrastructure/alembic
COPY alembic.ini ./

ENV RUN_CMD="gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"

EXPOSE 8000

CMD ["sh", "-c", "$RUN_CMD"]
