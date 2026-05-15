# Контрольная работа №2 — FastAPI

## 🛠 Установка

```powershell
cd C:\Users\vacti\Music\Serv2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 Запуск

```cmd
uvicorn main:app --reload
```

Документация (Swagger UI): <http://localhost:8000/docs>

## 📋 Маршруты

| Задание | Метод | Маршрут | Описание |
|---|---|---|---|
| 3.1 | POST | `/create_user` | Создание пользователя (валидация email, age > 0) |
| 3.2 | GET | `/product/{product_id}` | Товар по id |
| 3.2 | GET | `/products/search?keyword=&category=&limit=` | Поиск товаров |
| 5.1 | POST | `/v1/login` | Логин → cookie `session_token` (UUID) |
| 5.1 | GET | `/v1/user` | Профиль (401 без cookie) |
| 5.2 | POST | `/v2/login` | Логин → cookie с подписью `itsdangerous` |
| 5.2 | GET | `/v2/profile` | Профиль (проверка подписи) |
| 5.3 | POST | `/v3/login` | Логин → cookie `<uid>.<ts>.<sig>` |
| 5.3 | GET | `/v3/profile` | Профиль с динамическим продлением |
| 5.4 | GET | `/headers-simple` | Заголовки через параметры функции |
| 5.5 | GET | `/headers` | Заголовки через Pydantic-модель `CommonHeaders` |
| 5.5 | GET | `/info` | Приветствие + заголовки + `X-Server-Time` |

## 🧪 Тестовые учётные данные

Для всех заданий с авторизацией:
- `username`: `user123`, `password`: `password123`

## 🧪 Примеры запросов в Postman

### Задание 3.1 — POST `/create_user`

Body → raw → JSON:
```json
{
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30,
    "is_subscribed": true
}
```
Ожидаемо: вернётся то же самое. Если поставить `"email": "not-an-email"` или `"age": -5` — будет 422.

### Задание 3.2 — поиск товаров

GET `http://localhost:8000/products/search?keyword=phone&category=Electronics&limit=5`

Ожидаемо: список с `Smartphone` и `Iphone` (оба матчат "phone" и категорию Electronics).

GET `http://localhost:8000/product/123` — вернёт Smartphone.
GET `http://localhost:8000/product/999` — 404.

### Задания 5.1 / 5.2 / 5.3 — авторизация

**Важно:** в Postman включи передачу cookies — слева вверху рядом с URL есть ссылка **Cookies**, или используй вкладку **Cookies** под кнопкой Send. По умолчанию Postman сам хранит cookies между запросами, так что обычно ничего настраивать не нужно.

#### 5.1
1. POST `http://localhost:8000/v1/login` → Body → raw → JSON:
   ```json
   {"username": "user123", "password": "password123"}
   ```
   В ответе вкладка **Cookies** покажет `session_token=<UUID>`.

2. GET `http://localhost:8000/v1/user` → Send. Должен вернуться профиль.

3. Удали cookie вручную (Cookies → выбери `localhost` → удали `session_token`) → снова GET `/v1/user` → 401 `{"message": "Unauthorized"}`.

#### 5.2
То же, но URL — `/v2/login` и `/v2/profile`. В cookie значение будет в формате `<uuid>.<подпись>`. Если в Postman вручную поменять подпись и снова дёрнуть `/v2/profile` — получишь 401.

#### 5.3 (динамическое продление)
1. POST `/v3/login` → получаешь cookie с timestamp.
2. Сразу GET `/v3/profile` (прошло < 3 мин) → 200, cookie **не обновляется**.
3. Через 3+ минуты GET `/v3/profile` → 200, cookie **обновлена** (новый timestamp).
4. Через 5+ минут без активности → 401 `{"message": "Session expired"}`.
5. Подмена UUID или timestamp в cookie вручную → 401 `{"message": "Invalid session"}`.

> Для быстрой проверки можно временно уменьшить константы `SESSION_MAX_AGE` и `SESSION_REFRESH_AFTER` в `routers/auth_v3.py` (например, 30 и 18 секунд) — логика не изменится, а тестировать удобнее.

### Задание 5.4 — GET `/headers-simple`

Postman сам добавит `User-Agent` (`PostmanRuntime/...`). Чтобы сработала валидация Accept-Language, добавь его руками:

Вкладка **Headers**:
| Key | Value |
|---|---|
| Accept-Language | `en-US,en;q=0.9,ru;q=0.8` |

Если убрать `Accept-Language` (снять галку) → 400.
Если поставить кривое значение, например `###` → 400 «invalid format».

### Задание 5.5 — GET `/headers` и `/info`

Те же заголовки. Для `/info` посмотри в ответе вкладку **Headers** — там будет `X-Server-Time` со временем сервера, плюс в теле JSON с приветствием.

## 📁 Структура проекта

```
Serv2/
├── main.py              # точка входа, собирает роутеры
├── models.py            # все Pydantic-модели
├── data.py              # тестовые товары (3.2)
├── requirements.txt
├── README.md
└── routers/
    ├── __init__.py
    ├── users.py         # 3.1
    ├── products.py      # 3.2
    ├── auth_v1.py       # 5.1
    ├── auth_v2.py       # 5.2
    ├── auth_v3.py       # 5.3
    └── headers.py       # 5.4 + 5.5
```
