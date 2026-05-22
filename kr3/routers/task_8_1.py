"""
Задание 8.1.
POST /register сохраняет username и password в SQLite (таблица users).
Без SQLAlchemy, как в условии. Пароль в открытом виде — тоже по условию.
"""

from fastapi import APIRouter

from database import get_db_connection
from models import SimpleUser

router = APIRouter(prefix="/task8_1", tags=["Задание 8.1 — SQLite users"])


@router.post("/register")
async def register(user: SimpleUser):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, user.password),
        )
        conn.commit()
    finally:
        conn.close()
    return {"message": "User registered successfully!"}


@router.get("/users")
async def list_users():
    """Для удобной самопроверки."""
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT id, username FROM users").fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]
