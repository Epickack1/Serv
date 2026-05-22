"""
Общие утилиты для аутентификации (DRY для заданий 6.2 → 6.5).
"""

from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

# bcrypt-контекст для всех заданий, где есть хеш паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT-настройки (для заданий 6.4, 6.5, 7.1)
JWT_SECRET = "kr3-jwt-secret-please-change-in-prod"
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 30


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(payload: dict, expires_minutes: int = JWT_EXPIRES_MINUTES) -> str:
    data = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    data["exp"] = expire
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Бросает jwt.ExpiredSignatureError / jwt.InvalidTokenError."""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
