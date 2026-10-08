# PrestaShop DB test framework

Тестовый фреймворк на `pytest` + [PyMySQL](https://pypi.org/project/PyMySQL/)
для работы с базой данных MySQL магазина PrestaShop (таблица `ps_customer`).

## Структура

```
.
├── conftest.py            # pytest_addoption + фикстура connection
├── lib/
│   ├── db.py              # функции для работы с таблицей ps_customer
│   └── data.py            # фабрика данных нового клиента
├── tests/
│   ├── conftest.py        # фикстуры customer_data и existing_customer
│   └── test_customer.py   # тестовые сценарии
├── pytest.ini
└── requirements.txt
```

## Установка

```bash
pip install -r requirements.txt
```

## Параметры подключения

Параметры соединения задаются через опции pytest:

| Опция        | По умолчанию | Описание        |
| ------------ | ------------ | --------------- |
| `--host`     | `127.0.0.1`  | Хост MySQL      |
| `--port`     | `3306`       | Порт MySQL      |
| `--database` | `prestashop` | Имя базы данных |
| `--user`     | `root`       | Пользователь    |
| `--password` | *(пусто)*    | Пароль          |

Фикстура `connection` (scope `session`) открывает одно соединение на весь
прогон и закрывает его по завершении.

## Запуск

```bash
pytest --host=127.0.0.1 --port=3306 --database=prestashop --user=root --password=secret
```

## Тестовые сценарии

1. Создание нового клиента и проверка его наличия в БД по `id`.
2. Обновление `firstname`, `lastname`, `email` существующего клиента и
   проверка изменений.
3. Негативный тест: обновление несуществующего клиента (0 изменённых строк).
4. Удаление существующего клиента и проверка отсутствия в БД.
5. Негативный тест: удаление несуществующего клиента (0 изменённых строк).
