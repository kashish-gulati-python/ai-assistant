from sqlalchemy.orm import Session
from app.schemas.auth import RegisterUserRequest, LoginUserRequest
from app.models.user import Users
from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.db.deps import get_db
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError
from uuid import UUID

security = HTTPBearer(auto_error=False)

def register_user(db: Session, request: RegisterUserRequest) -> Users:
    hashed_password = hash_password(request.password)
    user = Users(name=request.name, email=request.email, password_hash=hashed_password)
    db.add(user)
    db.commit()
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
    return db.query(Users).first()

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    token = credentials.credentials

    try:
        user_id = UUID(decode_access_token(token))
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.get(Users, user_id)
    if user is None:
        raise credentials_exception

    return user
