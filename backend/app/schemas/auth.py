from pydantic import BaseModel, EmailStr, field_validator, Field, StringConstraints
from uuid import UUID
from datetime import datetime
from typing import Annotated

class RegisterUserRequest(BaseModel):
    name: str = Annotated[str, StringConstraints(..., min_length=3, max_length=50, strip_whitespace=True)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=60)]

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return value.lower()
    
    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if not any(c.isupper() for c in value) or any(c.isdigit() for c in value):
          raise ValueError("Password must contain at least one uppercase letter and one digit")
        return value
    
class RegisterUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class MeResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
