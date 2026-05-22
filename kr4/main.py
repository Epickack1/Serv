from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from exceptions import register_exception_handlers
from models import ErrorResponse
from routers import task_9_1, task_10_1, task_10_2, task_11

app = FastAPI(title="Контрольная работа №4")

# Задание 10.1 — кастомные исключения
register_exception_handlers(app)


# Задание 10.2 — кастомный обработчик ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    # Собираем человекочитаемое сообщение из errors()
    fields = []
    for err in exc.errors():
        loc = ".".join(str(p) for p in err.get("loc", []) if p != "body")
        fields.append({"field": loc, "message": err.get("msg"), "type": err.get("type")})

    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "Request payload validation failed",
            "status_code": 422,
            "details": fields,
        },
    )


app.include_router(task_9_1.router)
app.include_router(task_10_1.router)
app.include_router(task_10_2.router)
app.include_router(task_11.router)


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "КР4 — FastAPI. Документация: /docs",
        "tasks": {
            "9.1": "POST /products, GET /products, GET /products/{id} (миграции через Alembic)",
            "10.1": "GET /task10_1/check/{value}, GET /task10_1/items/{id} (custom exceptions)",
            "10.2": "POST /task10_2/users (Pydantic validation + кастомный обработчик)",
            "11.1": "Тесты см. tests/test_users_sync.py (pytest + TestClient)",
            "11.2": "Тесты см. tests/test_users_async.py (pytest-asyncio + httpx + Faker)",
        },
    }
