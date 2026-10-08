"""Фикстуры с данными клиента для тестовых сценариев."""

from __future__ import annotations

import pytest

from lib.data import build_customer_data
from lib.db import create_customer, delete_customer


@pytest.fixture
def customer_data() -> dict:
    """Данные нового клиента, которого ещё нет в базе."""
    return build_customer_data()


@pytest.fixture
def existing_customer(connection, customer_data) -> int:
    """Создаёт клиента в базе и удаляет его после теста."""
    customer_id = create_customer(connection, customer_data)
    yield customer_id
    delete_customer(connection, customer_id)
