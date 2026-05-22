import os

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from database import init_db
from routers import (
    task_6_1,
    task_6_2,
    task_6_3,
    task_6_4,
    task_6_5,
    task_7_1,
    task_8_1,
    task_8_2,
)
from routers.task_6_3 import configure_docs
from routers.task_6_5 import limiter

MODE = os.getenv("MODE", "DEV").upper()

# В PROD полностью гасим встроенные адреса документации.
# В DEV отключаем только дефолтные адреса /docs и /openapi.json — их
# заново подцепит configure_docs() уже с Basic-аутентификацией,
# а /redoc по условию должен быть скрыт.
if MODE == "PROD":
    app = FastAPI(
        title="Контрольная работа №3",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
else:
    app = FastAPI(
        title="Контрольная работа №3",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

# Защищённый /docs (только для DEV)
configure_docs(app)

# Rate limiter из задания 6.5
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
async def on_startup():
    # Создаём таблицы для заданий 8.1 / 8.2
    init_db()


app.include_router(task_6_1.router)
app.include_router(task_6_2.router)
app.include_router(task_6_4.router)
app.include_router(task_6_5.router)
app.include_router(task_7_1.router)
app.include_router(task_8_1.router)
app.include_router(task_8_2.router)


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "КР3 — FastAPI. Документация: /docs (в DEV под Basic, в PROD недоступна)",
        "mode": MODE,
        "tasks": {
            "6.1": "GET /task6_1/login (Basic)",
            "6.2": "POST /task6_2/register, GET /task6_2/login (Basic + bcrypt)",
            "6.3": "GET /docs — DEV: под Basic; PROD: 404",
            "6.4": "POST /task6_4/login, GET /task6_4/protected_resource (JWT)",
            "6.5": "POST /task6_5/register, POST /task6_5/login, GET /task6_5/protected_resource (JWT + rate-limit)",
            "7.1": "POST /task7_1/register, POST /task7_1/login, /task7_1/resources, /task7_1/protected_resource (RBAC)",
            "8.1": "POST /task8_1/register, GET /task8_1/users (SQLite)",
            "8.2": "CRUD /task8_2/todos (SQLite)",
        },
    }
