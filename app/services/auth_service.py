from sqlalchemy.orm import Session
from app.schemas.auth import RegisterUserRequest, RegisterUserResponse
from app.models.user import Users
from app.core.security import hash_password

def register_user(db: Session, request: RegisterUserRequest) -> Users:
    hashed_password = hash_password(request.password)
    user = Users(name=request.name, email=request.email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(Users).first()
