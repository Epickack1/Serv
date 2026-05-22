# Контрольная работа №4

Задания 9.1, 10.1, 10.2, 11.1, 11.2. FastAPI, Alembic, кастомные исключения, валидация, тесты.

## Установка

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

## Задание 9.1 — миграции Alembic

Alembic уже инициализирован в репозитории, в `alembic/versions/` лежат две миграции:

- `0001_create_products` — создаёт таблицу `products` с полями `id, title, price, count`;
- `0002_add_description` — добавляет колонку `description` (`NOT NULL`).

### Применить миграции к чистой БД

```bash
alembic upgrade head
```

Появится файл `kr4.db`. Проверить, что в таблице есть колонка `description`, можно
через DB Browser for SQLite или из питона.

### Добавить две записи (см. условие задания)

После применения **первой** миграции (`alembic upgrade 0001_create_products`)
запустите сервер и добавьте две записи:

```bash
uvicorn main:app --reload
```

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"title":"Apple","price":1.5,"count":10,"description":"-"}' \
     http://localhost:8000/products

curl -X POST -H "Content-Type: application/json" \
     -d '{"title":"Bread","price":2.0,"count":5,"description":"-"}' \
     http://localhost:8000/products
```

> Если хотите воспроизвести историю миграций один-в-один по условию (две записи
> после первой миграции, затем накатить вторую) — временно уберите поле `description`
> из `ProductCreate` в `models.py` и из колонки в `db_models.py` перед applying 0001.
> В готовом коде модель уже отражает финальное состояние схемы (после 0002), это
> упрощает проверку. При желании сгенерировать новую миграцию автоматически:
>
> ```bash
> alembic revision --autogenerate -m "your message"
> ```

### Откат

```bash
alembic downgrade -1            # откатить последнюю миграцию
alembic downgrade base          # сбросить полностью
```

## Задание 10.1 — кастомные исключения

```bash
curl -i http://localhost:8000/task10_1/check/-5     # 418 CustomExceptionA
curl -i http://localhost:8000/task10_1/items/999    # 404 CustomExceptionB
curl http://localhost:8000/task10_1/items/1         # 200 OK
```

Формат ответа об ошибке (Pydantic-модель `ErrorResponse`):
```json
{"error":"CustomExceptionA","message":"...","status_code":418}
```

## Задание 10.2 — валидация Pydantic + кастомный обработчик

```bash
# валидный запрос
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"john","age":25,"email":"john@example.com","password":"secret12"}' \
     http://localhost:8000/task10_2/users

# невалидный (age=15, короткий password) — 422 с понятным телом
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"john","age":15,"email":"bad","password":"123"}' \
     http://localhost:8000/task10_2/users
```

Ответ при ошибке валидации:
```json
{
  "error": "ValidationError",
  "message": "Request payload validation failed",
  "status_code": 422,
  "details": [
    {"field":"age","message":"Input should be greater than 18","type":"greater_than"},
    ...
  ]
}
```

## Задания 11.1 и 11.2 — тесты

```bash
pytest -v
```

- `tests/test_users_sync.py` — задание 11.1: pytest + `TestClient`, тестовые классы,
  параметризация невалидных payload'ов.
- `tests/test_users_async.py` — задание 11.2: `pytest-asyncio` + `httpx.AsyncClient`
  через `ASGITransport`, данные через `Faker`. Покрыты 201/200/404/204/повторный
  delete → 404.
- Изоляция состояния — фикстура `_isolate_state` в `tests/conftest.py`,
  очищает in-memory словарь до и после каждого теста.

## Структура проекта

```
kr4/
├── main.py
├── models.py
├── db_models.py
├── exceptions.py
├── requirements.txt
├── pytest.ini
├── alembic.ini
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 0001_create_products.py
│       └── 0002_add_description.py
├── routers/
│   ├── task_9_1.py
│   ├── task_10_1.py
│   ├── task_10_2.py
│   └── task_11.py
└── tests/
    ├── conftest.py
    ├── test_users_sync.py
    └── test_users_async.py
```
