from fastapi import FastAPI
from fastapi.responses import FileResponse

from models import (
    Feedback,
    FeedbackSimple,
    User,
    UserWithAge,
)

app = FastAPI(title="Контрольная работа №1")



@app.get("/")
async def get_index():
    return FileResponse("index.html")



@app.post("/calculate")
async def calculate(num1: float, num2: float):

    return {"result": num1 + num2}



current_user = User(name="Двуреченский Всеволод", id=1)


@app.get("/users")
async def get_user():
    return current_user


@app.post("/user")
async def check_adult(user: UserWithAge):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18,
    }


feedbacks: list[Feedback] = []


@app.post("/feedback")
async def post_feedback(feedback: Feedback):
    feedbacks.append(feedback)
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}


feedbacks_simple: list[FeedbackSimple] = []


@app.post("/feedback-simple")
async def post_feedback_simple(feedback: FeedbackSimple):
    feedbacks_simple.append(feedback)
    return {"message": f"Feedback received. Thank you, {feedback.name}."}


@app.get("/feedbacks")
async def list_feedbacks():
    return feedbacks
