## Sprint 1: 1-June - 15 June tasks

### 1. Duplicate email registration returns 500

`backend/app/services/auth_service.py`

```
def register_user(db: Session, request: RegisterUserRequest) -> Users:
    hashed_password = hash_password(request.password)
    user = Users(name=request.name, email=request.email, password_hash=hashed_password)
    db.add(user)
    db.commit()   # ← UniqueViolation if email exists
```

#### fixed
```
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def register_user(db: Session, request: RegisterUserRequest) -> Users:
    hashed_password = hash_password(request.password)
    user = Users(name=request.name, email=request.email, password_hash=hashed_password)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    db.refresh(user)
    return user
```

### 2. Correct primary keys on Conversations and Messages

`backend/app/models/user.py`

```
# Conversations — user_id is PK, not the conversation's own id
user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, ...)
id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)

# Messages — foreign key (with a typo) is PK, not the message's own id
convesation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, ...)
id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
```
This means we can only store one conversation per user (PK collision on second insert) and one message per conversation. The correct structure:

```
class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

### 3. deleted_at defaults to NOW — every row is born "deleted"

`backend/app/models/user.py`

```
deleted_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
```
Any query filtering WHERE deleted_at IS NULL returns zero rows. The column should be nullable with no default:
```
deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

### 4. No foreign keys defined on Conversations or Messages

`backend/app/models/user.py:17-34`

Neither model has `ForeignKey(...)` declarations. The database has no referential integrity — you can insert a `Conversation` pointing to a non-existent `user_id` and it will succeed.