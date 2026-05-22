"""
Задание 8.2.
CRUD для Todo (SQLite). Используем тот же database.py, таблица todos
создаётся в init_db() при старте.
"""

from fastapi import APIRouter, HTTPException, status

from database import get_db_connection
from models import TodoCreate, TodoOut, TodoUpdate

router = APIRouter(prefix="/task8_2/todos", tags=["Задание 8.2 — Todo CRUD"])


def _row_to_todo(row) -> TodoOut:
    return TodoOut(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        completed=bool(row["completed"]),
    )


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
async def create_todo(payload: TodoCreate):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO todos (title, description, completed) VALUES (?, ?, 0)",
            (payload.title, payload.description),
        )
        conn.commit()
        new_id = cur.lastrowid
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (new_id,)).fetchone()
    finally:
        conn.close()
    return _row_to_todo(row)


@router.get("/{todo_id}", response_model=TodoOut)
async def get_todo(todo_id: int):
    conn = get_db_connection()
    try:
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    finally:
        conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return _row_to_todo(row)


@router.get("", response_model=list[TodoOut])
async def list_todos():
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
    finally:
        conn.close()
    return [_row_to_todo(r) for r in rows]


@router.put("/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: int, payload: TodoUpdate):
    conn = get_db_connection()
    try:
        existing = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        new_title = payload.title if payload.title is not None else existing["title"]
        new_desc = payload.description if payload.description is not None else existing["description"]
        new_done = payload.completed if payload.completed is not None else bool(existing["completed"])

        conn.execute(
            "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
            (new_title, new_desc, int(new_done), todo_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    finally:
        conn.close()
    return _row_to_todo(row)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    conn = get_db_connection()
    try:
        existing = conn.execute("SELECT id FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
    finally:
        conn.close()
    return {"message": f"Todo {todo_id} deleted"}
