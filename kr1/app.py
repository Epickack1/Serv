
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Моя контрольная работа№1"}