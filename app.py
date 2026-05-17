from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel

from models import User, UserAge, Feedback, FeedbackValidated


app = FastAPI(title="Контрольная работа №1 — FastAPI — Egor Trunov")


@app.get("/welcome")
def welcome():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}


@app.get("/", response_class=HTMLResponse)
def read_index():
    return FileResponse("index.html")

class CalcInput(BaseModel):
    num1: float
    num2: float


@app.post("/calculate")
def calculate(data: CalcInput):
    result = data.num1 + data.num2
    if data.num1 == int(data.num1) and data.num2 == int(data.num2):
        result = int(result)
    return {"result": result}


current_user = User(name="Egor Trunov", id=1)


@app.get("/users")
def get_users():
    return current_user


@app.post("/user")
def check_user(user: UserAge):
    is_adult = user.age >= 18
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult,
    }

feedbacks: list[FeedbackValidated] = []


@app.post("/feedback")
def post_feedback(feedback: FeedbackValidated):

    feedbacks.append(feedback)
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}


@app.get("/feedbacks")
def list_feedbacks():
    return feedbacks
