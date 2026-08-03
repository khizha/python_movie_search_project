from rich.table import Table
from pymongo.errors import PyMongoError

from constants import SEARCH_TYPE_NAMES
from formatters import format_search_params
from mongo_logger import (
    get_recent_searches,
    get_popular_searches,
)
from ui_utils import console, wait_for_enter
from validators import get_integer

def show_recent_searches():
    """
    Показывает последние поисковые запросы из MongoDB.

    Пользователь указывает количество записей,
    после чего результаты выводятся в виде таблицы.
    """
    while True:
        results_number = get_integer(
            "\nВведите желаемое количество запросов: "
        )

        if results_number > 0:
            break

        console.print("\nКоличество запросов должно быть больше нуля.")

    try:
        results = get_recent_searches(results_number)

    except PyMongoError:
        console.print(
            "\nНе удалось получить историю поиска."
        )
        wait_for_enter()
        return

    if not results:
        console.print("\nНичего не найдено.")
    else:
        table = Table(title="Последние запросы")

        table.add_column("№", justify="right")
        table.add_column("Тип запроса")
        table.add_column("Параметры")
        table.add_column("Найдено фильмов")
        table.add_column("Время")

        for index, item in enumerate(results, start=1):

            search_type = SEARCH_TYPE_NAMES[item["search_type"]]
            query = format_search_params(item)

            table.add_row(
                str(index),
                search_type,
                query,
                str(item["results_count"]),
                item["created_at"].strftime("%d.%m.%Y %H:%M"),
            )

        console.print(table)


def show_popular_searches():
    """
    Показывает самые популярные поисковые запросы из MongoDB.

    Результаты сортируются и выводятся в виде таблицы.
    """
    try:
        results = get_popular_searches()

    except PyMongoError:
        console.print("\nНе удалось получить список популярных запросов.")
        wait_for_enter()
        return

    if not results:
        console.print("\nНичего не найдено.")
    else:

        table = Table(title="Top-5 популярных запросов")

        table.add_column("№", justify="right")
        table.add_column("Тип запроса")
        table.add_column("Параметры")
        table.add_column("Количество запросов")

        for index, item in enumerate(results, start=1):

            search_type = SEARCH_TYPE_NAMES[item["search_type"]]
            query = format_search_params(item)

            table.add_row(
                str(index),
                search_type,
                query,
                str(item["requests_count"]),
            )

        console.print(table)
