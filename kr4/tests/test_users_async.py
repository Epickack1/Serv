"""
Задание 11.2.
Асинхронные тесты: pytest-asyncio + httpx.AsyncClient через ASGITransport
+ Faker для генерации данных. Без запуска uvicorn — обращения идут прямо
в ASGI-приложение.
"""

import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient

from main import app

faker = Faker()
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def _fake_user_payload() -> dict:
    return {"username": faker.user_name(), "age": faker.random_int(min=1, max=99)}


class TestCreateUserAsync:
    async def test_create_user_returns_201(self, client):
        payload = _fake_user_payload()
        response = await client.post("/users", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["id"] >= 1
        assert body["username"] == payload["username"]
        assert body["age"] == payload["age"]

    async def test_create_multiple_users_unique_ids(self, client):
        ids = set()
        for _ in range(5):
            r = await client.post("/users", json=_fake_user_payload())
            ids.add(r.json()["id"])
        assert len(ids) == 5

    async def test_create_user_invalid_age_type_returns_422(self, client):
        payload = {"username": faker.user_name(), "age": faker.word()}
        response = await client.post("/users", json=payload)
        assert response.status_code == 422


class TestGetUserAsync:
    async def test_get_existing_user_returns_200(self, client):
        created = (await client.post("/users", json=_fake_user_payload())).json()
        response = await client.get(f"/users/{created['id']}")
        assert response.status_code == 200
        assert response.json() == created

    async def test_get_unknown_user_returns_404(self, client):
        unknown_id = faker.random_int(min=10_000, max=99_999)
        response = await client.get(f"/users/{unknown_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}


class TestDeleteUserAsync:
    async def test_delete_existing_user_returns_204(self, client):
        created = (await client.post("/users", json=_fake_user_payload())).json()
        response = await client.delete(f"/users/{created['id']}")
        assert response.status_code == 204

    async def test_delete_then_delete_again_returns_404(self, client):
        """Сценарий из условия: повторное удаление того же пользователя -> 404."""
        created = (await client.post("/users", json=_fake_user_payload())).json()
        first = await client.delete(f"/users/{created['id']}")
        second = await client.delete(f"/users/{created['id']}")
        assert first.status_code == 204
        assert second.status_code == 404

    async def test_delete_then_get_returns_404(self, client):
        created = (await client.post("/users", json=_fake_user_payload())).json()
        await client.delete(f"/users/{created['id']}")
        get_after = await client.get(f"/users/{created['id']}")
        assert get_after.status_code == 404
