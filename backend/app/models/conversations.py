from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime, ForeignKey
from app.db.base import Base
from datetime import datetime, UTC
import uuid

class Conversations(Base):
    __tablename__ = "conversations"
    conversation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

class Messages(Base):
    __tablename__ = "messages"
    message_id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    conversation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.conversation_id"), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
<<<<<<< HEAD
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
=======
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
>>>>>>> 0f270ed18d981bc6d770cb07a8d903005cd46388
