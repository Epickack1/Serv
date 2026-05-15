import hashlib
import hmac
import time
import uuid

from fastapi import APIRouter, Cookie, HTTPException, Response

from models import LoginRequest

router = APIRouter(prefix="/v3", tags=["Задание 5.3 — dynamic session"])

SECRET_KEY = b"super-secret-key-for-kr2-task-5-3"

SESSION_MAX_AGE = 300
SESSION_REFRESH_AFTER = 180 

USERS = {
    "Всеволод": {
        "password": "123",
        "profile": {"username": "Всеволод", "name": "Ну эт я", "email": "test@gmail.com"},
    },
}

user_id_to_username: dict[str, str] = {}


def _sign(user_id: str, timestamp: int) -> str:
    msg = f"{user_id}.{timestamp}".encode()
    return hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()


def _build_token(user_id: str, timestamp: int) -> str:
    return f"{user_id}.{timestamp}.{_sign(user_id, timestamp)}"


def _parse_token(token: str) -> tuple[str, int, str] | None:
    parts = token.split(".")
    if len(parts) != 3:
        return None
    user_id, ts_str, signature = parts
    try:
        timestamp = int(ts_str)
    except ValueError:
        return None
    return user_id, timestamp, signature


def _set_session_cookie(response: Response, user_id: str, timestamp: int) -> None:
    response.set_cookie(
        key="session_token",
        value=_build_token(user_id, timestamp),
        httponly=True,
        secure=False,
        max_age=SESSION_MAX_AGE,
    )


@router.post("/login")
async def login(creds: LoginRequest, response: Response):
    user = USERS.get(creds.username)
    if not user or user["password"] != creds.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid.uuid4())
    user_id_to_username[user_id] = creds.username

    _set_session_cookie(response, user_id, int(time.time()))
    return {"message": "Login successful"}


@router.get("/profile")
async def profile(
    response: Response,
    session_token: str | None = Cookie(default=None),
):
    if session_token is None:
        response.status_code = 401
        return {"message": "Unauthorized"}

    parsed = _parse_token(session_token)
    if parsed is None:
        response.status_code = 401
        return {"message": "Invalid session"}

    user_id, timestamp, signature = parsed

    expected_sig = _sign(user_id, timestamp)
    if not hmac.compare_digest(expected_sig, signature):
        response.status_code = 401
        return {"message": "Invalid session"}

    username = user_id_to_username.get(user_id)
    if not username:
        response.status_code = 401
        return {"message": "Invalid session"}

    now = int(time.time())
    elapsed = now - timestamp

    if elapsed >= SESSION_MAX_AGE:
        response.status_code = 401
        return {"message": "Session expired"}

    if elapsed >= SESSION_REFRESH_AFTER:
        _set_session_cookie(response, user_id, now)

    return USERS[username]["profile"]
