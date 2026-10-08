"""Генерация корректных данных для ``ps_customer``."""

from __future__ import annotations

import hashlib
import uuid


def build_customer_data(**overrides) -> dict:
    """Полный набор данных нового клиента с уникальными полями.

    При каждом вызове генерируются случайные email, пароль и secure key,
    поэтому клиент всегда уникален. Любое поле можно переопределить
    именованным аргументом.
    """
    unique = uuid.uuid4().hex

    data = {
        "id_shop_group": 1,
        "id_shop": 1,
        "id_gender": 1,
        "id_default_group": 1,
        "id_lang": 1,
        "id_risk": 1,
        "firstname": "John",
        "lastname": "Doe",
        "email": f"john.doe.{unique[:12]}@example.com",
        "passwd": hashlib.md5(unique.encode()).hexdigest(),
        "secure_key": unique,
        "active": 1,
    }
    data.update(overrides)
    return data
