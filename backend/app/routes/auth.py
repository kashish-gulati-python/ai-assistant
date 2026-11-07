from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.dependencies.auth import get_current_user
from app.models.user import Users
from app.schemas.auth import (
    LoginUserRequest,
    LoginUserResponse,
    MeResponse,
    RegisterUserRequest,
    RegisterUserResponse,
)
from app.services.auth_service import get_user, get_users, register_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterUserResponse, status_code=201)
def register(request: RegisterUserRequest, db: Session=Depends(get_db)):
    user = register_user(db, request)
    return RegisterUserResponse(user_id=user.user_id, email=user.email, created_at=user.created_at)

@router.post("/login", response_model=LoginUserResponse)
def login(request: LoginUserRequest, db: Session=Depends(get_db)):
    user = get_user(db, request)
    return user

@router.get("/me", response_model=MeResponse)
def get_profile(current_user: Users=Depends(get_current_user)):
    return MeResponse(
        user_id=current_user.user_id,
        name=current_user.name,
        email=current_user.email,
        created_at=current_user.created_at,
    )


# Only for testing
@router.get('/all')
def get_all_users(db: Session=Depends(get_db)):
    return get_users(db)
