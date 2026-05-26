# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

AI Assistant is a FastAPI-based backend for a chat application. The v0.1 scope includes user authentication (registration/login/logout), conversation management, and message history. No LLM integration or advanced features are implemented yet.

## Tech Stack

- **Framework**: FastAPI 0.136.1
- **Database**: PostgreSQL 16 with SQLAlchemy 2.0+ ORM
- **Authentication**: JWT tokens with argon2 password hashing (passlib)
- **Server**: Uvicorn 0.47.0
- **Python Version**: 3.13 (uv as package manager)
- **Containerization**: Docker + docker-compose

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app initialization and router registration
│   ├── api/                    # Legacy API layer (minimal usage)
│   ├── routes/                 # Route handlers with dependency injection
│   │   └── auth.py             # Auth endpoints registration
│   ├── services/               # Business logic layer
│   │   └── auth_service.py     # User registration and queries
│   ├── schemas/                # Pydantic request/response models
│   │   └── auth.py
│   ├── models/                 # SQLAlchemy ORM models
│   │   └── user.py             # Users, Conversations, Messages models
│   ├── core/                   # Core utilities
│   │   └── security.py         # Password hashing functions
│   └── db/                     # Database configuration
│       ├── base.py             # Declarative base for models
│       └── session.py          # SQLAlchemy engine and SessionLocal
├── Dockerfile
├── docker-compose.yml          # PostgreSQL + API services
├── pyproject.toml              # Dependencies and project metadata
├── uv.lock                     # Locked dependency versions
└── README.md                   # API contracts and feature scope

```

## Architecture

The codebase follows a layered architecture:

1. **Routes** (app/routes/) - Handle HTTP requests, dependency injection
2. **Services** (app/services/) - Contain business logic, database operations
3. **Schemas** (app/schemas/) - Pydantic models for request validation and response serialization
4. **Models** (app/models/) - SQLAlchemy ORM definitions
5. **Core** (app/core/) - Utility functions (security, etc.)
6. **DB** (app/db/) - Database configuration and session management

The main.py file is minimal and only includes router registration. All routes are defined in app/routes/.

## Database Schema

Three main tables (note: schema may have issues - see Known Issues):
- **users**: id (UUID), name, email (unique), password_hash, created_at, updated_at
- **conversations**: id (UUID), user_id (FK), title, created_at, updated_at, deleted_at
- **messages**: id (UUID), conversation_id (FK), role, content, created_at, updated_at, deleted_at

Indexes on conversations(user_id) and messages(conversation_id).

## Running Locally

### Development with Docker
```bash
cd backend
docker-compose up --build
```
The API runs at http://localhost:8000 with hot reload enabled.

### Development without Docker
Requires Python 3.13 and a running PostgreSQL instance:
```bash
cd backend
uv pip install --system -r pyproject.toml
export DATABASE_URL=postgresql://postgres:password@localhost:5432/ai-assistant-db
uv run uvicorn app.main:app --reload
```

### Database
PostgreSQL is configured in docker-compose.yml:
- User: postgres
- Password: password
- Database: ai-assistant-db
- Port: 5432

## Testing

No test infrastructure is currently set up. The README mentions integration tests against a PostgreSQL test database should be written using pytest and FastAPI TestClient, but no tests exist yet.

To add tests:
```bash
uv pip install pytest pytest-asyncio httpx
```

## API Endpoints (v0.1 scope)

**Auth**:
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (not yet implemented)
- `POST /auth/logout` - Logout (not yet implemented)
- `GET /auth/me` - Get current user profile

**Conversations**:
- `POST /conversations` - Create conversation (not yet implemented)
- `GET /conversations` - List conversations (not yet implemented)
- `GET /conversations/{id}` - Get conversation details (not yet implemented)
- `DELETE /conversations/{id}` - Delete conversation (not yet implemented)

**Messages**:
- `POST /conversations/{id}/messages` - Add message (not yet implemented)
- `GET /conversations/{id}/messages` - Get messages (not yet implemented)

See README.md for detailed API contracts.

## Known Issues

1. **Models**: The Conversations and Messages models have inconsistent primary key definitions. Currently `user_id` and `conversation_id` are marked as primary keys instead of `id`. This will cause database issues and should be fixed.

2. **Schema duplication**: MeResponse has `name` defined twice.

3. **Implementation incomplete**: Only registration endpoint is partially implemented. Login, logout, and all conversation/message endpoints need implementation.

4. **Security**: JWT token logic and refresh token handling not yet implemented.

5. **Environment variables**: Database URL is hardcoded in db/session.py instead of using environment variables.

## Development Workflow

1. Modify app code in the appropriate layer (routes → services → models)
2. Update schemas in app/schemas/ for new request/response types
3. Add new models to app/models/user.py as needed
4. Create new route files in app/routes/ and register them in main.py
5. Restart the development server or docker-compose for changes to take effect

## Dependencies Management

This project uses `uv` as the package manager and lock file manager:
- Add new dependencies to pyproject.toml
- Run `uv pip install --system -r pyproject.toml` to install
- `uv.lock` tracks exact versions and should be committed

