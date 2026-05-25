from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.auth import RegisterUserRequest, RegisterUserResponse, MeResponse
from app.services.auth_service import register_user, get_users

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=RegisterUserResponse)
def register(request: RegisterUserRequest, db: Session=Depends(get_db)):
    user = register_user(db, request)
    return RegisterUserResponse(id=user.id, email=user.email, created_at=user.created_at)

@router.get("/me", response_model=MeResponse)
def retrieve(db: Session=Depends(get_db)):
    return get_users(db)
