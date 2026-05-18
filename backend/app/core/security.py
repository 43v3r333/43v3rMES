from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from backend.app.core.config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_access_token(subject, expires_delta=None):
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return jwt.encode({"exp": expire, "sub": str(subject)}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
def verify_password(plain, hashed): return pwd_context.verify(plain, hashed)
def get_password_hash(password): return pwd_context.hash(password)
