import re

from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    name: str
    id: int

class UserWithAge(BaseModel):
    name: str
    age: int


class FeedbackSimple(BaseModel):
    name: str
    message: str


FORBIDDEN_WORDS = ["кринж", "рофл", "вайб"]


class Feedback(BaseModel):

    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator("message")
    @classmethod
    def check_forbidden_words(cls, value: str) -> str:
        pattern = re.compile(
            r"\b(" + "|".join(FORBIDDEN_WORDS) + r")\w*",
            re.IGNORECASE,
        )
        if pattern.search(value):
            raise ValueError("Использование недопустимых слов")
        return value
