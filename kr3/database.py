"""
SQLite-подключение для заданий 8.1 и 8.2. Без SQLAlchemy, как и просит условие.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "kr3.db"


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Создаёт таблицы, если их ещё нет. Вызывается один раз при старте."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Задание 8.1
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    # Задание 8.2
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    conn.commit()
    conn.close()
