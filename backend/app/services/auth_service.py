from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.auth import RegisterUserRequest, LoginUserRequest
from app.models.user import Users
from app.core.security import create_access_token, hash_password, verify_password
from fastapi import HTTPException

def register_user(db: Session, request: RegisterUserRequest) -> Users:
    hashed_password = hash_password(request.password)
    user = Users(name=request.name, email=request.email, password_hash=hashed_password)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    db.refresh(user)
    return user

def get_user(db: Session, request: LoginUserRequest) -> dict[str, str]:
    user = db.query(Users).filter(Users.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(plain=request.password, hashed=user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(subject=str(user.user_id))
    return {"access_token": access_token, "token_type": "bearer"}

def get_users(db: Session):
    return db.query(Users).all()