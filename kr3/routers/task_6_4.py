"""
Задание 6.4.
JWT-аутентификация. /login возвращает токен, /protected_resource
требует валидный Bearer-токен в заголовке Authorization.
"""

import random

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models import LoginRequest, TokenResponse
from security import create_access_token, decode_access_token

router = APIRouter(prefix="/task6_4", tags=["Задание 6.4 — JWT (базовый)"])

bearer_scheme = HTTPBearer(auto_error=False)


def authenticate_user(username: str, password: str) -> bool:
    """
    Заглушка из условия: random.choice([True, False]).
    Чтобы можно было осмысленно тестировать — раскомментируйте проверку
    конкретных учёток ниже и закомментируйте random.choice.
    """
    # if username == "john_doe" and password == "securepassword123":
    #     return True
    # return False
    return random.choice([True, False])


@router.post("/login", response_model=TokenResponse)
async def login(creds: LoginRequest):
    if not authenticate_user(creds.username, creds.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": creds.username})
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
    return {"message": f"Access granted, {username}"}
