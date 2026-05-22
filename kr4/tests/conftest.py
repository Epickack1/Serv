"""
Общая фикстура — очистка in-memory хранилища до и после каждого теста.
Подключается автоматически для всех тестов в директории.
"""

import pytest

from routers.task_11 import reset_state


@pytest.fixture(autouse=True)
def _isolate_state():
    reset_state()
    yield
    reset_state()
