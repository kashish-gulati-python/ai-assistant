## Sprint 1: 1-June - 15 June tasks

### 1. Hardcoded credentials committed to the repository

`backend/alembic.ini`

```
sqlalchemy.url = postgresql+psycopg://postgres:password@localhost:5432/ai-assistant-db

Replace with a placeholder string that cannot pass connection validation:

sqlalchemy.url = postgresql+psycopg://CHANGE_ME:CHANGE_ME@localhost:5432/CHANGE_ME
```

### 2. POST /register returns 200 instead of 201

`backend/app/routes/auth.py`

```
# current
@router.post("/register", response_model=RegisterUserResponse)

# fixed
@router.post("/register", response_model=RegisterUserResponse, status_code=201)
```
`201 Created` must be returned when a new resource is created. Clients and API gateways key off status codes.

### 3. Missing verify_password in security.py

`backend/app/core/security.py`

Login is impossible to implement correctly without this function. Add it now alongside hash_password:

```
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```