from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from app.db.base import Base
from datetime import datetime, UTC
import uuid

class Users(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    email = Column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))

class Conversations(Base):
    __tablename__ = "conversations"
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
    deleted_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))

class Messages(Base):
    __tablename__ = "messages"
    convesation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
    deleted_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))