from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class RegisterUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class RegisterUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str

class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class MeResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
