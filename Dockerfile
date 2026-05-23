FROM python:3.12-slim

WORKDIR /code

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv pip install --system -r pyproject.toml

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--hostCOPY app/ ./app/", "0.0.0.0", "--port", "8000"]