"""
Задание 10.2. Pydantic-валидация + кастомный обработчик RequestValidationError.
Сам обработчик регистрируется в main.py (нужен FastAPI-инстанс).
"""

from fastapi import APIRouter

from models import UserPayload

router = APIRouter(prefix="/task10_2", tags=["Задание 10.2 — validation"])


@router.post("/users")
async def create_user(user: UserPayload):
    return {"message": "User accepted", "user": user.model_dump()}
