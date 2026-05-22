from typing import Optional

from pydantic import BaseModel, Field


# ===== Задание 6.2 — модели пользователя =====
class UserBase(BaseModel):
    username: str


class User(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


# ===== Задание 6.4 / 6.5 — JWT login =====
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ===== Задание 7.1 — RBAC =====
class RBACUserCreate(BaseModel):
    username: str
    password: str
    role: str = Field(default="guest", description="admin / user / guest")


# ===== Задание 8.2 — Todo CRUD =====
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = None


class TodoOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


# ===== Задание 8.1 — простая регистрация =====
class SimpleUser(BaseModel):
    username: str
    password: str
