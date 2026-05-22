"""
Эндпоинты для заданий 11.1 и 11.2: создание / получение / удаление пользователя
в in-memory словаре. Используются в tests/test_users_sync.py (pytest + TestClient)
и tests/test_users_async.py (pytest-asyncio + httpx.AsyncClient).
"""

from itertools import count
from threading import Lock

from fastapi import APIRouter, HTTPException, Response

from models import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["Задания 11.1 / 11.2 — tests"])

# In-memory хранилище; для изоляции в тестах его очищают через фикстуру.
db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()


def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


def reset_state() -> None:
    """Используется тестами для изоляции."""
    global _id_seq
    db.clear()
    _id_seq = count(start=1)


@router.post("", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    user_id = next_user_id()
    db[user_id] = user.model_dump()
    return {"id": user_id, **db[user_id]}


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
