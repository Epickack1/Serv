"""
Задание 6.5.
Расширенный JWT: регистрация с bcrypt, /login проверяет хеш,
/protected_resource требует Bearer. Rate-limit через slowapi:
/register — 1/мин, /login — 5/мин.
"""

import secrets

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address

from models import LoginRequest, TokenResponse, User, UserInDB
from security import create_access_token, decode_access_token, hash_password, verify_password

# limiter создаётся здесь, а к приложению цепляется в main.py
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/task6_5", tags=["Задание 6.5 — JWT + rate-limit"])

bearer_scheme = HTTPBearer(auto_error=False)

# in-memory БД
fake_users_db: dict[str, UserInDB] = {}


def _find_user(username: str) -> UserInDB | None:
    """Поиск пользователя со сравнением username через secrets.compare_digest."""
    for stored_username, stored_user in fake_users_db.items():
        if secrets.compare_digest(stored_username, username):
            return stored_user
    return None


@router.post("/register", status_code=201)
@limiter.limit("1/minute")
async def register(request: Request, user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=409, detail="User already exists")

    fake_users_db[user.username] = UserInDB(
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    return {"message": "New user created"}


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, creds: LoginRequest):
    user = _find_user(creds.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Authorization failed")

    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return username


@router.get("/protected_resource")
async def protected_resource(username: str = Depends(get_current_user)):
    return {"message": "Access granted", "username": username}
