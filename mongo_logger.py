from datetime import datetime
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from local_settings import (
    MONGODB_URL_WRITE,
    DATABASE_WRITE,
    MONGODB_COLLECTION,
)

import logging
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler(
    "error.log",
    encoding="utf-8",
    delay=True  # объект обработчика создаётся; файл не создаётся сразу, а появится только при первой записи через logger.error().
)

file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

def connect() -> MongoClient:
    """
        Создает подключение к серверу MongoDB.

        Использует строку подключения, указанную в настройках проекта.

        :return: Объект клиента MongoDB.
    """
    return MongoClient(MONGODB_URL_WRITE)


def get_collection() -> tuple[MongoClient, Collection]:
    """
        Возвращает подключение к MongoDB и коллекцию для хранения истории поиска.

        Подключается к серверу MongoDB, открывает базу данных,
        указанную в настройках проекта, и возвращает объект коллекции.
        Закрытие подключения выполняется вызывающей функцией.

        :return: Кортеж, содержащий объект клиента MongoDB и объект коллекции.
    """
    client = connect()
    db = client[DATABASE_WRITE]
    collection = db[MONGODB_COLLECTION]
    return client, collection


def log_mongo_errors(default_return):
    """
    Декоратор для обработки ошибок MongoDB.
    Возвращает указанное значение при ошибке.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except PyMongoError as error:
                logger.error(
                    f"Ошибка MongoDB в функции {func.__name__}: {error}"
                )
                return default_return

        return wrapper

    return decorator

@log_mongo_errors(None)
def save_search_log(
    search_type: str,
    search_params: dict[str, Any],
    results_count: int,
) -> None:
    """
    Сохраняет информацию о выполненном поисковом запросе в MongoDB.

    Формирует документ с типом поиска, параметрами запроса,
    количеством найденных результатов и временем выполнения поиска,
    после чего записывает его в коллекцию MongoDB.

    :param search_type: Тип поиска (например, "keyword",
        "category_name_and_year").
    :param search_params: Параметры поискового запроса.
    :param results_count: Количество найденных фильмов.
    :return: None.
    """
    client = None

    try:
        client, collection = get_collection()

        document = {
            "search_type": search_type,
            "search_params": search_params,
            "results_count": results_count,
            "created_at": datetime.now(),
        }

        collection.insert_one(document)

    finally:
        if client:
            client.close()


@log_mongo_errors([])
def get_popular_searches() -> list[dict[str, Any]]:
    """
    Возвращает список из пяти самых популярных поисковых запросов.

    Популярность определяется частотой выполнения одинаковых запросов.
    Запрос считается одинаковым, если совпадают его тип (`search_type`)
    и параметры (`search_params`).

    :return: Список словарей с информацией о популярных поисковых запросах.
    """
    client = None

    try:
        client, collection = get_collection()

        # aggregation pipeline
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "search_type": "$search_type",
                        "search_params": "$search_params",
                    },
                    "requests_count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                   "requests_count": -1
                }
            },
            {
                "$limit": 5
            },
            {
                "$project": {
                    "_id": 0,
                    "search_type": "$_id.search_type",
                    "search_params": "$_id.search_params",
                    "requests_count": 1,
                }
            }
        ]
        result = collection.aggregate(pipeline)

        return list(result)

    finally:
        if client:
            client.close()

@log_mongo_errors([])
def get_recent_searches(limit: int = 5) -> list[dict[str, Any]]:
    """
    Возвращает список последних поисковых запросов.

    Запросы сортируются по времени выполнения в порядке убывания.

    :param limit: Максимальное количество записей.
    :return: Список последних поисковых запросов.
    """
    client = None

    try:
        client, collection = get_collection()

        pipeline = [
            {
                "$sort": {
                    "created_at": -1
                }
            },
            {
                "$limit": limit
            },
            {
                "$project": {
                    "_id": 0,
                    "search_type": 1,
                    "search_params": 1,
                    "results_count": 1,
                    "created_at": 1,
                }
            }
        ]

        result = collection.aggregate(pipeline)

        return list(result)

    finally:
        if client:
            client.close()