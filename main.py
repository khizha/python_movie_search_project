# Panel создает рамку вокруг текста
from rich.panel import Panel

# Align отвечает за выравнивание текста и объектов
from rich.align import Align

# Table создает таблицы
from rich.table import Table

from ui_utils import  console, wait_for_enter
from validators import get_integer, get_integer_in_range
from constants import SEARCH_TYPE_NAMES
from formatters import format_search_params

import os
import mysql.connector
from pymongo.errors import PyMongoError

from mysql_connector import get_films_by_keyword
from mysql_connector import get_categories_with_years
from mysql_connector import get_films_by_category_id_and_year

from mongo_logger import get_recent_searches
from mongo_logger import save_search_log
from mongo_logger import get_popular_searches


def clear_screen():
    """
    Очищает экран терминала.
    """
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    """
    Выводит главное меню приложения.
    """

    # Очищаем консоль перед показом меню
    #console.clear()

    # Создаем текстовое содержимое меню
    menu = (
        "1. Поиск по ключевому слову\n"
        "2. Поиск по жанру и диапазону годов выпуска\n"
        #"3. Список годов\n"
        #"4. Список жанров\n"
        "3. Последние запросы\n"
        "4. Популярные запросы\n"
        "\n"
        "0. Выход"
    )

    # Создаем объект Panel
    # Panel отвечает только за внешний вид рамки
    panel = Panel(
        # Центрируем текст внутри панели
        Align.center(menu),

        # Заголовок
        title="ПОИСК ФИЛЬМОВ",

        # Цвет рамки
        border_style="bright_white",

        # Фиксированная ширина панели в символах
        width=55,

        # Внутренние отступы:
        # сверху и снизу, слева и справа.
        padding=(1, 4)
    )

    # Выводим готовую панель в консоль
    console.print(

        # Центрируем рамку (объект Panel)
        Align(
            panel,
            align="center",
            vertical="middle"
        )
    )


def main() -> None:
    """
    Запускает главное меню приложения.
    """

    while True:

        clear_screen()
        show_menu()

        choice = console.input("\nВыберите пункт меню: ").strip()

        if choice == "1":
            show_search_by_keyword()

        elif choice == "2":
            show_search_by_category()


        elif choice == "3":
            show_recent_searches()
            wait_for_enter()

        elif choice == "4":
            show_popular_searches()
            wait_for_enter()

        elif choice == "0":
            clear_screen()
            # console.print("До свидания!")
            break

        else:
            console.print("\nНекорректный выбор. Попробуйте снова.")
            console.input("\nНажмите Enter для продолжения...")

        #wait_for_enter()

def show_films_in_pages(films):
    """
    Показывает фильмы порциями по 10 штук.
    Пользователь может запросить следующую страницу
    или вернуться в меню.
    """

    if not films:
        console.print("\nНичего не найдено.")
        wait_for_enter()
        return

    page_size = 10
    start = 0

    while start < len(films):

        end = start + page_size

        console.print(
            f"\nПоказаны фильмы {start + 1}-{min(end, len(films))}"
            f" из {len(films)}"
        )

        # for film in films[start:end]:
            # print(
            #     f"{film['title']} ({film['release_year']})"
            # )
        table = Table(title="Результаты поиска")

        table.add_column("№", justify="right")
        table.add_column("Название")
        table.add_column("Год", justify="center")

        for index, film in enumerate(films[start:end], start=start + 1):
            table.add_row(
    str(index),
               film["title"],
               str(film["release_year"]),
            )

        console.print(table)

        # если показали последнюю страницу
        if end >= len(films):
            console.print("\n-=Конец списка.=-")
            wait_for_enter()
            break

        while True:
            choice = console.input(
                "\nПоказать следующие 10 фильмов? (Enter — да, 0 — меню): "
            ).strip()

            if choice == "":
                start = end
                break

            if choice == "0":
                return

            console.print("\nНекорректный выбор. Попробуйте снова.")


def show_search_by_keyword():

    keyword = console.input("\nВведите ключевое слово: ").strip()

    if not keyword:
        console.print("\nКлючевое слово не может быть пустым.")
        wait_for_enter()
        return

    try:
        films = get_films_by_keyword(keyword)


    except mysql.connector.Error as error:
        console.print(
            f"\nНе удалось выполнить поиск.\n"
            f"Причина: {error}"
        )
        wait_for_enter()
        return

    save_search_log(
        search_type="keyword",
        search_params={"keyword": keyword},
        results_count=len(films)
    )

    show_films_in_pages(films)

def show_search_by_category():
    try:
        categories = get_categories_with_years()

    except mysql.connector.Error:
        console.print("\nНе удалось получить список жанров. Ошибка подключения к базе данных.")
        wait_for_enter()
        return

    if not categories:
        console.print("\nНичего не найдено.")
        wait_for_enter()
        return
    else:

        table = Table(title="Доступные жанры")

        table.add_column("№", justify="right")
        table.add_column("Жанр")
        table.add_column("Годы", justify="center")

        for index, item in enumerate(categories, start=1):
            table.add_row(
                str(index),
                item["category"],
                f'{item["first_year"]} – {item["last_year"]}',
            )

        console.print(table)

        # выбор жанра
        choice = get_integer_in_range(
            "\nВведите номер жанра: ",
            1,
            len(categories),
            "Некорректный выбор. Попробуйте снова.",
        )

        selected = categories[choice - 1] # выбранный жанр (словарь!)
        category_id = selected["category_id"]
        category_name = selected["category"]
        first_year = selected["first_year"]
        last_year = selected["last_year"]

        console.print(f"\nВыбран жанр: {category_name}")
        console.print(f"Доступные годы: {first_year} - {last_year}")

        year_from = get_integer_in_range(
            f"\nВведите начальный год ({first_year}-{last_year}): ",
            first_year,
            last_year,
        )

        while True:
            year_to = get_integer_in_range(
                f"Введите конечный год ({first_year}-{last_year}): ",
                first_year,
                last_year,
            )

            if year_to < year_from:
                console.print(
                    "\nКонечный год не может быть меньше начального."
                )
                continue

            break

        try:
            films = get_films_by_category_id_and_year(
                category_id,
                year_from,
                year_to
            )

        except mysql.connector.Error:
            console.print(
                "\nНе удалось выполнить поиск. Ошибка подключения к базе данных."
            )
            wait_for_enter()
            return

        show_films_in_pages(films)

        save_search_log(
            search_type="category_name_and_year",
            search_params={
                "category_name": category_name,
                "year_from": year_from,
                "year_to": year_to,
            },
            results_count=len(films),
        )


def show_recent_searches():
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

            #query = format_search_description(item)

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
                #item["search_type"],
                search_type,
                query,
                str(item["requests_count"]),
            )

        console.print(table)


if __name__ == "__main__":

    main()
