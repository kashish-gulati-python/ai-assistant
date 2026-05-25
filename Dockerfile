FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv pip install --system .

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]