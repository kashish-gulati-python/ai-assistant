## Overview

AI Assistant is a FastAPI-based backend for a chat application. The v0.1 scope includes user authentication (registration/login/logout), conversation management, and message history. No LLM integration or advanced features are implemented yet.

## Tech Stack

- **Framework**: FastAPI 0.136.1
- **Database**: PostgreSQL 16 with SQLAlchemy 2.0+ ORM and Alembic migrations
- **Authentication**: JWT tokens via `python-jose`, argon2 password hashing via `passlib`
- **DB Driver**: `psycopg` v3 (binary) — connection strings use `postgresql+psycopg://`
- **Server**: Uvicorn 0.47.0
- **Python Version**: 3.13, managed by `uv`
- **Containerization**: Docker + docker-compose

### Setup

Copy `.env.example` to `.env` and fill in values. docker-compose reads these at runtime.

```bash
cp backend/.env.example backend/.env
```

### With Docker
```bash
cd backend
docker-compose up --build
```

API runs at http://localhost:8000 with hot reload.

### Without Docker

Requires Python 3.13 and a running PostgreSQL instance.

```bash
cd backend
uv sync
# Set DATABASE_URL in .env or export it directly
uv run uvicorn app.main:app --reload
```

## Database Migrations (Alembic)

All schema changes go through Alembic. Run from `backend/`:

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Generate a new migration from model changes
uv run alembic revision --autogenerate -m "describe change"

# Downgrade one step
uv run alembic downgrade -1
```

`alembic/env.py` reads `DATABASE_URL` from the environment, overriding `alembic.ini`'s hardcoded fallback. Always set `DATABASE_URL` when running migrations against a non-default DB.

## Architecture

Layered: **Routes → Services → Models**, with Schemas for validation and Core for utilities.

- `app/routes/` — HTTP handlers, dependency injection (`get_db` is currently defined locally in each route file, not a shared module)
- `app/services/` — business logic and DB queries
- `app/schemas/` — Pydantic request/response models
- `app/models/user.py` — all three SQLAlchemy models (Users, Conversations, Messages)
- `app/core/security.py` — password hashing only; JWT logic not yet implemented
- `app/db/session.py` — engine and `SessionLocal`; reads `DATABASE_URL` from env with a localhost fallback
- `app/api/` — legacy/unused layer; ignore

`main.py` only registers routers. New route files go in `app/routes/` and must be registered there.