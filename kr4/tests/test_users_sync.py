"""
Задание 11.1.
Синхронные модульные тесты на pytest + fastapi.testclient.TestClient
для трёх эндпоинтов из task_11: POST /users, GET /users/{id}, DELETE /users/{id}.
"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestCreateUser:
    def test_create_user_returns_201_and_valid_body(self):
        response = client.post("/users", json={"username": "alice", "age": 25})
        assert response.status_code == 201
        body = response.json()
        assert body == {"id": 1, "username": "alice", "age": 25}

    def test_create_user_assigns_incrementing_ids(self):
        first = client.post("/users", json={"username": "a", "age": 20}).json()
        second = client.post("/users", json={"username": "b", "age": 21}).json()
        assert second["id"] == first["id"] + 1

    @pytest.mark.parametrize("payload", [
        {"username": "x"},               # нет age
        {"age": 30},                     # нет username
        {"username": "x", "age": "abc"}, # age не int
        {},                              # совсем пусто
    ])
    def test_create_user_invalid_payload_returns_422(self, payload):
        response = client.post("/users", json=payload)
        assert response.status_code == 422


class TestGetUser:
    def test_get_existing_user_returns_200(self):
        created = client.post("/users", json={"username": "bob", "age": 30}).json()
        response = client.get(f"/users/{created['id']}")
        assert response.status_code == 200
        assert response.json() == created

    def test_get_unknown_user_returns_404(self):
        response = client.get("/users/99999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_get_user_with_invalid_id_type_returns_422(self):
        response = client.get("/users/not-a-number")
        assert response.status_code == 422


class TestDeleteUser:
    def test_delete_existing_user_returns_204(self):
        created = client.post("/users", json={"username": "carol", "age": 40}).json()
        response = client.delete(f"/users/{created['id']}")
        assert response.status_code == 204
        assert response.content == b""

    def test_delete_then_get_returns_404(self):
        created = client.post("/users", json={"username": "dave", "age": 22}).json()
        client.delete(f"/users/{created['id']}")
        assert client.get(f"/users/{created['id']}").status_code == 404

    def test_delete_unknown_user_returns_404(self):
        response = client.delete("/users/424242")
        assert response.status_code == 404
