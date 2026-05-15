from fastapi import APIRouter

from models import UserCreate

router = APIRouter(tags=["Задание 3.1"])


@router.post("/create_user")
async def create_user(user: UserCreate):
    return user
