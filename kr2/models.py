import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# UserCreate
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: Optional[int] = Field(default=None, gt=0)
    is_subscribed: Optional[bool] = False


# Product
class Product(BaseModel):
    """Модель товара."""
    product_id: int
    name: str
    category: str
    price: float


# Модель логина
class LoginRequest(BaseModel):
    """Тело запроса для логина."""
    username: str
    password: str


# Модель заголовков
# Регулярка для валидации Accept-Language, например: "en-US,en;q=0.9,es;q=0.8"
ACCEPT_LANGUAGE_RE = re.compile(
    r"^[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})?(;q=\d(\.\d+)?)?"
    r"(,\s*[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})?(;q=\d(\.\d+)?)?)*$"
)


class CommonHeaders(BaseModel):
    user_agent: str = Field(..., alias="User-Agent")
    accept_language: str = Field(..., alias="Accept-Language")

    model_config = {"populate_by_name": True}

    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, value: str) -> str:
        if not ACCEPT_LANGUAGE_RE.match(value):
            raise ValueError("Неверный формат Accept-Language")
        return value
