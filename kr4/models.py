"""
Pydantic-модели для КР4.
SQLAlchemy-модели (задание 9.1) — в отдельном файле db_models.py.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, conint, constr


# ===== Задание 9.1 — Product API =====
class ProductCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    count: int = Field(..., ge=0)
    description: str = Field(..., min_length=1)


class ProductOut(ProductCreate):
    id: int

    model_config = {"from_attributes": True}


# ===== Задание 10.1 — ответ об ошибке =====
class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int


# ===== Задание 10.2 — пользовательские данные =====
class UserPayload(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


# ===== Задание 11.1 / 11.2 — простые модели =====
class UserIn(BaseModel):
    username: str
    age: int


class UserOut(BaseModel):
    id: int
    username: str
    age: int
