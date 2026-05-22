"""
Задание 6.3.
Управление доступом к /docs в зависимости от MODE (DEV/PROD).
Функции отсюда вызываются из main.py — там и кастомные маршруты,
здесь же только сама логика (чтобы main.py остался читабельным).
"""

import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials

docs_security = HTTPBasic()


def _read_mode() -> str:
    mode = os.getenv("MODE", "DEV").upper()
    if mode not in {"DEV", "PROD"}:
        raise RuntimeError(f"Invalid MODE='{mode}', expected DEV or PROD")
    return mode


def _check_docs_credentials(
    credentials: HTTPBasicCredentials = Depends(docs_security),
) -> str:
    expected_user = os.getenv("DOCS_USER", "docs")
    expected_pass = os.getenv("DOCS_PASSWORD", "docs")

    is_user_ok = secrets.compare_digest(credentials.username, expected_user)
    is_pass_ok = secrets.compare_digest(credentials.password, expected_pass)
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid docs credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def configure_docs(app: FastAPI) -> None:
    """
    Если MODE=PROD — /docs, /redoc, /openapi.json возвращают 404.
    Если MODE=DEV  — /docs и /openapi.json защищены HTTP Basic, /redoc отключён.
    """
    mode = _read_mode()

    if mode == "PROD":
        # в PROD ничего не подключаем — FastAPI инициализирован
        # с docs_url=None, redoc_url=None, openapi_url=None (см. main.py)
        return

    # DEV-режим: переопределяем /openapi.json и /docs, требуя Basic
    @app.get("/openapi.json", include_in_schema=False)
    async def openapi_json(_: str = Depends(_check_docs_credentials)):
        return app.openapi()

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger(_: str = Depends(_check_docs_credentials)):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=app.title + " — Swagger UI (DEV)",
        )
