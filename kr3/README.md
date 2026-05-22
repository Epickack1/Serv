# Контрольная работа №3

Задания 6.1 – 8.2. FastAPI, аутентификация (Basic/JWT), RBAC, SQLite.

## Установка

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # при необходимости поменять MODE / DOCS_USER / DOCS_PASSWORD
```

## Запуск

```bash
uvicorn main:app --reload
```

Документация в DEV-режиме: `http://localhost:8000/docs` (под Basic, креды из `.env`).
В PROD-режиме (`MODE=PROD`) `/docs`, `/redoc`, `/openapi.json` отдают 404.

## Проверка через curl

### Задание 6.1 — Basic auth
```bash
curl -u admin:wrong   http://localhost:8000/task6_1/login   # 401
curl -u admin:secret  http://localhost:8000/task6_1/login   # 200
```

### Задание 6.2 — bcrypt
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"user1","password":"correctpass"}' \
     http://localhost:8000/task6_2/register

curl -u user1:correctpass http://localhost:8000/task6_2/login   # 200
curl -u user1:wrong       http://localhost:8000/task6_2/login   # 401
```

### Задание 6.3 — DEV/PROD docs
DEV:
```bash
curl -u docs:docs http://localhost:8000/docs
```
PROD (запустить с `MODE=PROD uvicorn main:app`):
```bash
curl -i http://localhost:8000/docs   # 404
```

### Задание 6.4 — JWT
```bash
# authenticate_user — случайная (см. условие), может потребоваться несколько попыток
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"john_doe","password":"securepassword123"}' \
     http://localhost:8000/task6_4/login

curl -H "Authorization: Bearer <TOKEN>" \
     http://localhost:8000/task6_4/protected_resource
```

### Задание 6.5 — JWT + rate-limit
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"qwerty123"}' \
     http://localhost:8000/task6_5/register      # 201

curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"qwerty123"}' \
     http://localhost:8000/task6_5/login         # 200 + token

curl -H "Authorization: Bearer <TOKEN>" \
     http://localhost:8000/task6_5/protected_resource
```
Лимиты: `/register` — 1/мин, `/login` — 5/мин; при превышении 429.

### Задание 7.1 — RBAC
```bash
# admin
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"adm","password":"a","role":"admin"}' \
     http://localhost:8000/task7_1/register

# guest
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"gst","password":"g","role":"guest"}' \
     http://localhost:8000/task7_1/register

# логин и токен
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"adm","password":"a"}' \
     http://localhost:8000/task7_1/login

# admin может всё:
curl -H "Authorization: Bearer <ADMIN_TOKEN>" \
     -X POST -H "Content-Type: application/json" -d '{"name":"x"}' \
     http://localhost:8000/task7_1/resources

# guest может только читать (получит 403 на create/update/delete):
curl -H "Authorization: Bearer <GUEST_TOKEN>" \
     -X DELETE http://localhost:8000/task7_1/resources/1
```

### Задание 8.1 — SQLite users
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"test_user","password":"12345"}' \
     http://localhost:8000/task8_1/register
```

### Задание 8.2 — Todo CRUD
```bash
# create
curl -X POST -H "Content-Type: application/json" \
     -d '{"title":"Buy groceries","description":"Milk, eggs, bread"}' \
     http://localhost:8000/task8_2/todos

# read
curl http://localhost:8000/task8_2/todos/1

# update
curl -X PUT -H "Content-Type: application/json" \
     -d '{"completed":true}' \
     http://localhost:8000/task8_2/todos/1

# delete
curl -X DELETE http://localhost:8000/task8_2/todos/1
```

## Структура проекта

```
kr3/
├── main.py
├── database.py
├── security.py
├── models.py
├── requirements.txt
├── .env.example
└── routers/
    ├── task_6_1.py
    ├── task_6_2.py
    ├── task_6_3.py
    ├── task_6_4.py
    ├── task_6_5.py
    ├── task_7_1.py
    ├── task_8_1.py
    └── task_8_2.py
```
