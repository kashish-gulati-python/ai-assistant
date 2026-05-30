## Sprint 1: 1-June - 15 June tasks

### 1. Database credentials printed to stdout on every startup

`backend/app/db/session.py`

```
POSTGRES_DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:password@localhost:5432/ai-assistant-db")
print(POSTGRES_DB_URL)   # ← password in every log line
```

Remove the print entirely.

### 2. All DateTime defaults are evaluated once at import time

`backend/app/models/user.py`

```
created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
deleted_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
```

datetime.now(UTC) is a call expression — Python evaluates it once when the class body is parsed. Every row inserted gets the module-load timestamp. Use server_default for the DB to stamp it, or pass a callable:

```
from sqlalchemy import func

created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

### 3. No password validation — empty string is a valid password

`backend/app/schemas/auth.py`

```
# current
password: str
```
```
# fixed
from pydantic import field_validator
from typing import Annotated
from pydantic import Field

password: Annotated[str, Field(min_length=8, max_length=128)]

@field_validator("password")
@classmethod
def password_strength(cls, v: str) -> str:
    if not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
        raise ValueError("Password must contain at least one uppercase letter and one digit")
    return v
```

### 4. No input constraints on `name`

`backend/app/schemas/auth.py`

```
# current — empty string, 10MB string, all valid
name: str

# fixed
name: Annotated[str, Field(min_length=1, max_length=100, strip_whitespace=True)]
```