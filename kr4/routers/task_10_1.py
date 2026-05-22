"""
Задание 10.1. Эндпоинты, демонстрирующие пользовательские исключения.
"""

from fastapi import APIRouter

from exceptions import CustomExceptionA, CustomExceptionB

router = APIRouter(prefix="/task10_1", tags=["Задание 10.1 — custom exceptions"])

# фейковое хранилище
items: dict[int, dict] = {1: {"id": 1, "name": "Apple"}}


@router.get("/check/{value}")
async def check_value(value: int):
    """Если value < 0 — кидаем CustomExceptionA."""
    if value < 0:
        raise CustomExceptionA(f"Value must be non-negative, got {value}")
    return {"value": value, "ok": True}


@router.get("/items/{item_id}")
async def get_item(item_id: int):
    """Если item_id не найден — кидаем CustomExceptionB."""
    if item_id not in items:
        raise CustomExceptionB(f"Item with id={item_id} does not exist")
    return items[item_id]
