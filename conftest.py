"""Опции подключения к MySQL и фикстура ``connection``."""

from __future__ import annotations

import pymysql
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Регистрирует опции подключения к базе данных MySQL."""
    parser.addoption(
        "--host",
        action="store",
        default="127.0.0.1",
        help="Хост MySQL",
    )
    parser.addoption(
        "--port",
        action="store",
        type=int,
        default=3306,
        help="Порт MySQL",
    )
    parser.addoption(
        "--database",
        action="store",
        default="prestashop",
        help="Имя базы данных",
    )
    parser.addoption(
        "--user",
        action="store",
        default="root",
        help="Пользователь базы данных",
    )
    parser.addoption(
        "--password",
        action="store",
        default="",
        help="Пароль базы данных",
    )


@pytest.fixture(scope="session")
def connection(request: pytest.FixtureRequest) -> pymysql.connections.Connection:
    """Открывает соединение с MySQL на весь прогон тестов."""
    config = request.config
    db_connection = pymysql.connect(
        host=config.getoption("--host"),
        port=config.getoption("--port"),
        database=config.getoption("--database"),
        user=config.getoption("--user"),
        password=config.getoption("--password"),
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
    yield db_connection
    db_connection.close()
