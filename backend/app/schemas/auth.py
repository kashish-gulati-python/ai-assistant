from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class RegisterUserRequest(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=50, strip_whitespace=True)]
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return value.lower()
    
    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if not any(c.isupper() for c in value) or not any(c.isdigit() for c in value):
          raise ValueError("Password must contain at least one uppercase letter and one digit")
        return value
    
class RegisterUserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    created_at: datetime

class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str

class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class MeResponse(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr
    created_at: datetime
