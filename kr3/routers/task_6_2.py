"""
Задание 6.2.
Регистрация и логин с хешированием паролей (bcrypt) и in-memory БД.
"""

import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models import User, UserInDB
from security import hash_password, verify_password

router = APIRouter(prefix="/task6_2", tags=["Задание 6.2 — bcrypt"])

security = HTTPBasic()

# in-memory БД: username -> UserInDB
fake_users_db: dict[str, UserInDB] = {}


def auth_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserInDB:
    """
    Достаёт пользователя из fake_users_db, сравнивает хеш пароля.
    Username сверяется через secrets.compare_digest.
    """
    user = None
    for stored_username, stored_user in fake_users_db.items():
        if secrets.compare_digest(stored_username, credentials.username):
            user = stored_user
            break

    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


@router.post("/register", status_code=201)
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=409, detail="User already exists")

    fake_users_db[user.username] = UserInDB(
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    return {"message": f"User '{user.username}' successfully registered"}


@router.get("/login")
async def login(user: UserInDB = Depends(auth_user)):
    return {"message": f"Welcome, {user.username}!"}
