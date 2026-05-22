"""
Задание 7.1.
RBAC поверх JWT. Три роли: admin, user, guest.
"""

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models import LoginRequest, RBACUserCreate, TokenResponse, UserInDB
from security import create_access_token, decode_access_token, hash_password, verify_password

router = APIRouter(prefix="/task7_1", tags=["Задание 7.1 — RBAC"])

bearer_scheme = HTTPBearer(auto_error=False)

# Разрешения по ролям
PERMISSIONS = {
    "admin": {"create", "read", "update", "delete"},
    "user": {"read", "update"},
    "guest": {"read"},
}

# in-memory БД пользователей и ресурсов
users_db: dict[str, dict] = {}        # username -> {hashed_password, role}
resources_db: dict[int, dict] = {}    # id -> resource
_next_resource_id = 1


def _find_user(username: str) -> dict | None:
    return users_db.get(username)


@router.post("/register", status_code=201)
async def register(payload: RBACUserCreate):
    if payload.role not in PERMISSIONS:
        raise HTTPException(status_code=400, detail=f"Unknown role: {payload.role}")
    if payload.username in users_db:
        raise HTTPException(status_code=409, detail="User already exists")

    users_db[payload.username] = {
        "hashed_password": hash_password(payload.password),
        "role": payload.role,
    }
    return {"message": f"User '{payload.username}' registered as '{payload.role}'"}


@router.post("/login", response_model=TokenResponse)
async def login(creds: LoginRequest):
    user = _find_user(creds.username)
    if user is None or not verify_password(creds.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": creds.username, "role": user["role"]})
    return TokenResponse(access_token=token)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    role = payload.get("role")
    if not username or role not in PERMISSIONS:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {"username": username, "role": role}


def require_permission(action: str):
    """Фабрика зависимостей: проверяет, что роль текущего юзера имеет action."""

    def checker(user: dict = Depends(get_current_user)) -> dict:
        if action not in PERMISSIONS[user["role"]]:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{user['role']}' has no permission to '{action}'",
            )
        return user

    return checker


# ===== общая точка для админа и юзера =====
@router.get("/protected_resource")
async def protected_resource(user: dict = Depends(require_permission("read"))):
    return {
        "message": "Access granted",
        "username": user["username"],
        "role": user["role"],
        "permissions": sorted(PERMISSIONS[user["role"]]),
    }


# ===== эндпоинты по ролям =====
@router.post("/resources", status_code=201)
async def create_resource(
    data: dict,
    user: dict = Depends(require_permission("create")),
):
    global _next_resource_id
    rid = _next_resource_id
    _next_resource_id += 1
    resources_db[rid] = {"id": rid, **data, "created_by": user["username"]}
    return resources_db[rid]


@router.get("/resources")
async def list_resources(user: dict = Depends(require_permission("read"))):
    return list(resources_db.values())


@router.put("/resources/{rid}")
async def update_resource(
    rid: int,
    data: dict,
    user: dict = Depends(require_permission("update")),
):
    if rid not in resources_db:
        raise HTTPException(status_code=404, detail="Resource not found")
    resources_db[rid].update(data)
    return resources_db[rid]


@router.delete("/resources/{rid}")
async def delete_resource(
    rid: int,
    user: dict = Depends(require_permission("delete")),
):
    if rid not in resources_db:
        raise HTTPException(status_code=404, detail="Resource not found")
    del resources_db[rid]
    return {"message": f"Resource {rid} deleted"}
