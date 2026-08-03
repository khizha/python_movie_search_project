from rich.table import Table

from ui_utils import  console, wait_for_enter
from validators import get_integer, get_integer_in_range
from constants import SEARCH_TYPE_NAMES
from formatters import format_search_params
from search_service import (
    search_by_keyword,
    get_categories,
    search_by_category,
)
from display import show_films_in_pages
from menu import clear_screen, show_menu
from history import (
    show_recent_searches,
    show_popular_searches,
)


import mysql.connector

from mongo_logger import save_search_log


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


def show_search_by_keyword():

    keyword = console.input("\nВведите ключевое слово: ").strip()

    if not keyword:
        console.print("\nКлючевое слово не может быть пустым.")
        wait_for_enter()
        return

    try:
        films = search_by_keyword(keyword)

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
        categories = get_categories()

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
            films = search_by_category(
                category_id,
                year_from,
                year_to,
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


if __name__ == "__main__":

    main()
