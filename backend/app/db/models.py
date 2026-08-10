from sqlalchemy import Column, Uuid, String, DateTime, Integer
from app.db.database import Base
import uuid

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Conversations(Base):
    __tablename__ = "conversations"
    user_id = Column(Uuid, primary_key=True, index=True)
    id = Column(Uuid, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)

class Messages(Base):
    __tablename__ = "messages"
    convesation_id = Column(Uuid, primary_key=True, index=True)
    id = Column(Uuid, nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)