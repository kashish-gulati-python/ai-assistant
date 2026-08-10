from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterUserRequest, RegisterUserResponse, LoginUserRequest, LoginUserResponse, MeResponse
from app.services.auth_service import get_current_user, register_user, get_user
from app.db.deps import get_db
from app.models.user import Users

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterUserResponse, status_code=201)
def register(request: RegisterUserRequest, db: Session=Depends(get_db)):
    user = register_user(db, request)
    return RegisterUserResponse(id=user.id, email=user.email, created_at=user.created_at)

@router.post("/login", response_model=LoginUserResponse)
def login(request: LoginUserRequest, db: Session=Depends(get_db)):
    user = get_user(db, request)
    return user

@router.get("/me", response_model=MeResponse)
def retrieve(current_user: Users = Depends(get_current_user)):
    return current_user
