"""Тесты создания, обновления и удаления клиентов."""

from __future__ import annotations

from lib.data import build_customer_data
from lib.db import (
    create_customer,
    delete_customer,
    get_customer,
    get_next_customer_id,
    update_customer,
)


def test_create_customer(connection, customer_data):
    """Созданный клиент читается из базы по своему id."""
    customer_id = create_customer(connection, customer_data)
    try:
        assert customer_id > 0

        customer = get_customer(connection, customer_id)
        assert customer is not None
        assert customer["firstname"] == customer_data["firstname"]
        assert customer["lastname"] == customer_data["lastname"]
        assert customer["email"] == customer_data["email"]
    finally:
        delete_customer(connection, customer_id)


def test_update_customer(connection, existing_customer):
    """Обновлённые firstname, lastname и email сохраняются в базе."""
    new_data = {
        "firstname": "Jane",
        "lastname": "Smith",
        "email": build_customer_data()["email"],
    }

    affected = update_customer(connection, existing_customer, new_data)

    assert affected == 1
    customer = get_customer(connection, existing_customer)
    assert customer["firstname"] == new_data["firstname"]
    assert customer["lastname"] == new_data["lastname"]
    assert customer["email"] == new_data["email"]


def test_update_nonexistent_customer(connection):
    """Обновление несуществующего клиента не меняет ни одной строки."""
    missing_id = get_next_customer_id(connection)
    assert get_customer(connection, missing_id) is None

    affected = update_customer(connection, missing_id, {"firstname": "Ghost"})

    assert affected == 0


def test_delete_customer(connection, existing_customer):
    """Удалённый клиент пропадает из базы."""
    affected = delete_customer(connection, existing_customer)

    assert affected == 1
    assert get_customer(connection, existing_customer) is None


def test_delete_nonexistent_customer(connection):
    """Удаление несуществующего клиента не меняет ни одной строки."""
    missing_id = get_next_customer_id(connection)
    assert get_customer(connection, missing_id) is None

    affected = delete_customer(connection, missing_id)

    assert affected == 0
