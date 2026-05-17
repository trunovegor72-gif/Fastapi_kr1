from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def show(title, resp):
    print(f"\n=== {title} ===")
    print("status:", resp.status_code)
    try:
        print("json  :", resp.json())
    except Exception:
        print("text  :", resp.text[:200])


# 1.1 — /welcome
show("1.1 GET /welcome", client.get("/welcome"))

# 1.2 — / (HTML)
r = client.get("/")
print("\n=== 1.2 GET / (HTML) ===")
print("status:", r.status_code)
print("body  :", r.text.strip())

# 1.3* — /calculate
show("1.3* POST /calculate num1=5 num2=10",
     client.post("/calculate", json={"num1": 5, "num2": 10}))
show("1.3* POST /calculate num1=2.5 num2=0.5",
     client.post("/calculate", json={"num1": 2.5, "num2": 0.5}))

# 1.4 — /users
show("1.4 GET /users", client.get("/users"))

# 1.5* — /user
show("1.5* POST /user age=26", client.post("/user", json={"name": "Egor Trunov", "age": 26}))
show("1.5* POST /user age=15", client.post("/user", json={"name": "Kid", "age": 15}))

# 2.1 / 2.2* — /feedback (валидный)
show("2.2* POST /feedback (valid)",
     client.post("/feedback", json={"name": "Артур", "message": "Это тяжело, но я справлюсь!"}))

# 2.2* — /feedback (короткое имя + недопустимое слово -> 422)
show("2.2* POST /feedback (invalid)",
     client.post("/feedback", json={"name": "А", "message": "Какой-то кринж у вас тут происходит..."}))

# 2.2* — недопустимое слово в падеже
show("2.2* POST /feedback (forbidden word in case)",
     client.post("/feedback", json={"name": "Иван", "message": "Полный рофла этот семинар оказался"}))

# список отзывов
show("GET /feedbacks", client.get("/feedbacks"))

print("\nВсе проверки выполнены.")
