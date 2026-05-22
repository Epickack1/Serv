"""
Задание 6.1.
Защищённый /login с HTTP Basic. Учётные данные хардкодом
(в следующих заданиях добавим хеш и in-memory БД).
"""

import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/task6_1", tags=["Задание 6.1 — Basic auth"])

security = HTTPBasic()

VALID_USERNAME = "admin"
VALID_PASSWORD = "secret"


def authenticate(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    # secrets.compare_digest защищает от тайминг-атак
    is_user_ok = secrets.compare_digest(credentials.username, VALID_USERNAME)
    is_pass_ok = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/login")
async def login(username: str = Depends(authenticate)):
    return {"message": "You got my secret, welcome"}
