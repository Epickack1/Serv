import uuid

from fastapi import APIRouter, Cookie, HTTPException, Response
from itsdangerous import BadSignature, Signer

from models import LoginRequest

router = APIRouter(prefix="/v2", tags=["Задание 5.2 — signed cookie"])

SECRET_KEY = b"super-secret-key-for-kr2-task-5-2"
signer = Signer(SECRET_KEY)

USERS = {
    "Всеволод": {
        "password": "123",
        "profile": {"username": "Всеволод", "name": "Ну эт я", "email": "test@gmail.com"},
    },
}

user_id_to_username: dict[str, str] = {}


@router.post("/login")
async def login(creds: LoginRequest, response: Response):
    user = USERS.get(creds.username)
    if not user or user["password"] != creds.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid.uuid4())
    user_id_to_username[user_id] = creds.username

    signed = signer.sign(user_id).decode()

    response.set_cookie(
        key="session_token",
        value=signed,
        httponly=True,
        secure=False,
        max_age=3600,
    )
    return {"message": "Login successful"}


@router.get("/profile")
async def profile(
    response: Response,
    session_token: str | None = Cookie(default=None),
):
    if session_token is None:
        response.status_code = 401
        return {"message": "Unauthorized"}

    try:
        user_id_bytes = signer.unsign(session_token)
        user_id = user_id_bytes.decode()
    except BadSignature:
        response.status_code = 401
        return {"message": "Unauthorized"}

    username = user_id_to_username.get(user_id)
    if not username:
        response.status_code = 401
        return {"message": "Unauthorized"}

    return USERS[username]["profile"]
