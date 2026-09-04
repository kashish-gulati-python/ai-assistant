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

# class Messages(Base):
#     __tablename__ = "messages"
#     convesation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
#     message_id:  Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
#     role: Mapped[str] = mapped_column(String, nullable=False)
#     content: Mapped[str] = mapped_column(String, nullable=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
#     updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
#     deleted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))