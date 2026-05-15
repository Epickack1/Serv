# Контрольная работа №1 — FastAPI

Курс «Технологии разработки серверных приложений», 4 семестр 2025/2026.

## 🛠 Установка

1. Создайте виртуальное окружение и активируйте его:

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **Linux / macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Запуск

### Задание 1.1 — отдельное приложение в `app.py`
```bash
uvicorn app:app --reload
```
Откройте <http://localhost:8000> — увидите JSON-приветствие.

### Все остальные задания (1.2–2.2) — `main.py`
```bash
uvicorn main:app --reload
```

Документация (Swagger UI): <http://localhost:8000/docs>

## 📋 Что где находится

| Задание | Маршрут | Метод | Что делает |
|---|---|---|---|
| 1.1 | `/` (в `app.py`) | GET | Приветственный JSON |
| 1.2 | `/` (в `main.py`) | GET | Отдаёт `index.html` |
| 1.3 | `/calculate?num1=5&num2=10` | POST | Возвращает сумму: `{"result": 15}` |
| 1.4 | `/users` | GET | Данные текущего пользователя |
| 1.5 | `/user` | POST | Принимает JSON `{name, age}`, добавляет `is_adult` |
| 2.1 | `/feedback-simple` | POST | Простое сохранение отзыва без валидации |
| 2.2 | `/feedback` | POST | Отзыв с валидацией: длина полей + запрет слов «кринж», «рофл», «вайб» |
|  | `/feedbacks` | GET | Список всех валидированных отзывов |

## 🧪 Примеры запросов

### Задание 1.3 — POST `/calculate`
```bash
curl -X POST "http://localhost:8000/calculate?num1=5&num2=10"
# {"result": 15.0}
```

### Задание 1.5 — POST `/user`
```bash
curl -X POST http://localhost:8000/user \
  -H "Content-Type: application/json" \
  -d '{"name": "Артур", "age": 25}'
# {"name":"Артур","age":25,"is_adult":true}
```

### Задание 2.2 — POST `/feedback` (успех)
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{"name": "Артур", "message": "Это тяжело, но я справлюсь!"}'
# {"message":"Спасибо, Артур! Ваш отзыв сохранён."}
```

### Задание 2.2 — POST `/feedback` (валидация падает)
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{"name": "А", "message": "Какой-то кринж у вас тут происходит..."}'
# HTTP 422 + список ошибок
```
