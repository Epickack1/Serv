"""
Пользовательские исключения и их обработчики (задание 10.1).
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from models import ErrorResponse


class CustomExceptionA(Exception):
    """Бросаем, когда условие задачи не выполнено."""
    status_code = 418
    message = "Custom A: precondition failed"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.message


class CustomExceptionB(Exception):
    """Бросаем, когда ресурс не найден."""
    status_code = 404
    message = "Custom B: resource not found"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.message


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CustomExceptionA)
    async def handle_a(request: Request, exc: CustomExceptionA):
        print(f"[CustomExceptionA] {request.url.path} -> {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="CustomExceptionA",
                message=exc.detail,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(CustomExceptionB)
    async def handle_b(request: Request, exc: CustomExceptionB):
        print(f"[CustomExceptionB] {request.url.path} -> {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="CustomExceptionB",
                message=exc.detail,
                status_code=exc.status_code,
            ).model_dump(),
        )
