import re
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Response

from models import ACCEPT_LANGUAGE_RE, CommonHeaders

router = APIRouter(tags=["Задания 5.4 / 5.5 — headers"])


@router.get("/headers-simple")
async def headers_simple(
    user_agent: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header()] = None,
):
    if not user_agent:
        raise HTTPException(status_code=400, detail="Header 'User-Agent' is required")
    if not accept_language:
        raise HTTPException(status_code=400, detail="Header 'Accept-Language' is required")

    if not ACCEPT_LANGUAGE_RE.match(accept_language):
        raise HTTPException(
            status_code=400,
            detail="Header 'Accept-Language' has invalid format",
        )

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language,
    }

@router.get("/headers")
async def headers(common: Annotated[CommonHeaders, Header()]):
    return {
        "User-Agent": common.user_agent,
        "Accept-Language": common.accept_language,
    }


@router.get("/info")
async def info(common: Annotated[CommonHeaders, Header()], response: Response):
    response.headers["X-Server-Time"] = datetime.now().isoformat(timespec="seconds")
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": common.user_agent,
            "Accept-Language": common.accept_language,
        },
    }
