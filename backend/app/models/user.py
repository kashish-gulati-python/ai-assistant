from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from app.db.base import Base
from datetime import datetime, UTC
import uuid

class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    email = Column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))