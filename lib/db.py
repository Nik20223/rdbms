"""Работа с таблицей ``ps_customer`` в PrestaShop."""

from __future__ import annotations

from datetime import datetime

CUSTOMER_TABLE = "ps_customer"


def _timestamp() -> str:
    """Возвращает текущие дату и время в формате DATETIME."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_customer(connection, customer_data: dict) -> int:
    """Создаёт нового клиента и возвращает его ``id_customer``.

    В ``customer_data`` должны быть обязательные для ``ps_customer`` поля
    (``id_gender``, ``firstname``, ``lastname``, ``email`` и ``passwd``);
    ``date_add`` и ``date_upd`` заполняются автоматически.
    """
    data = dict(customer_data)
    now = _timestamp()
    data.setdefault("date_add", now)
    data.setdefault("date_upd", now)

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    query = f"INSERT INTO {CUSTOMER_TABLE} ({columns}) VALUES ({placeholders})"

    with connection.cursor() as cursor:
        cursor.execute(query, list(data.values()))
        return cursor.lastrowid


def get_customer(connection, customer_id: int) -> dict | None:
    """Возвращает клиента по id или ``None``, если его нет."""
    query = f"SELECT * FROM {CUSTOMER_TABLE} WHERE id_customer = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (customer_id,))
        return cursor.fetchone()


def update_customer(connection, customer_id: int, customer_data: dict) -> int:
    """Обновляет поля клиента и возвращает число затронутых строк.

    Значение ``0`` означает, что клиента с таким ``customer_id`` нет.
    """
    data = dict(customer_data)
    data.setdefault("date_upd", _timestamp())

    assignments = ", ".join(f"{column} = %s" for column in data)
    query = f"UPDATE {CUSTOMER_TABLE} SET {assignments} WHERE id_customer = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, [*data.values(), customer_id])
        return cursor.rowcount


def delete_customer(connection, customer_id: int) -> int:
    """Удаляет клиента и возвращает число затронутых строк.

    Значение ``0`` означает, что клиента с таким ``customer_id`` нет.
    """
    query = f"DELETE FROM {CUSTOMER_TABLE} WHERE id_customer = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (customer_id,))
        return cursor.rowcount


def get_next_customer_id(connection) -> int:
    """Возвращает ещё не занятый ``id_customer``."""
    query = f"SELECT COALESCE(MAX(id_customer), 0) + 1 AS next_id FROM {CUSTOMER_TABLE}"
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()["next_id"]
