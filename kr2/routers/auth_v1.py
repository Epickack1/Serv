import uuid

from fastapi import APIRouter, Cookie, HTTPException, Response

from models import LoginRequest

router = APIRouter(prefix="/v1", tags=["Задание 5.1 — cookie auth (UUID)"])

USERS = {
    "Всеволод": {
        "password": "123",
        "profile": {"username": "Всеволод", "name": "Ну эт я", "email": "test@gmail.com"},
    },
    "admin": {
        "password": "admin",
        "profile": {"username": "admin", "name": "Administrator", "email": "admin@gmail.com"},
    },
}

sessions: dict[str, str] = {}


@router.post("/login")
async def login(creds: LoginRequest, response: Response):
    user = USERS.get(creds.username)
    if not user or user["password"] != creds.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = str(uuid.uuid4())
    sessions[token] = creds.username

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,
        max_age=3600,
    )
    return {"message": "Login successful"}


@router.get("/user")
async def get_user(
    response: Response,
    session_token: str | None = Cookie(default=None),
):
    if session_token is None or session_token not in sessions:
        response.status_code = 401
        return {"message": "Unauthorized"}

    username = sessions[session_token]
    return USERS[username]["profile"]
