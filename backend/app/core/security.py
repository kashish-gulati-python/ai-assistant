from passlib.context import CryptContext
from datetime import datetime, UTC, timedelta
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)

def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    sub = payload.get("sub")
    if sub is None:
        raise JWTError("Missing sub claim")
    return sub