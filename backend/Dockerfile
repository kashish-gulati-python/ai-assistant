FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv pip install --system .

COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]