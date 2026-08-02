# Импортируем основной объект Rich для вывода информации в консоль
from rich.console import Console

# Panel создает рамку вокруг текста
from rich.panel import Panel

# Align отвечает за выравнивание текста и объектов
from rich.align import Align

# Table создает таблицы
from rich.table import Table

import os

from mysql_connector import get_films_by_keyword
from mysql_connector import get_categories_with_years
from mysql_connector import get_films_by_category_id_and_year

from mongo_logger import get_recent_searches
from mongo_logger import save_search_log
from mongo_logger import get_popular_searches

SEARCH_TYPE_NAMES = {
    "keyword": "Ключевое слово",
    "category_name_and_year": "Жанр и годы",
    "category_id_and_year": "ID жанра и годы",
}

# Создаем объект консоли
# Через него будем выводить все элементы Rich
console = Console()

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
        "2. Поиск по жанру  и диапазону годов выпуска\n"
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

        choice = input("\nВыберите пункт меню: ")

        if choice == "1":
            show_search_by_keyword()

        elif choice == "2":
            show_search_by_category()


        elif choice == "3":
            show_recent_searches()
            console.input("\nНажмите Enter для возврата в меню...")

        elif choice == "4":
            show_popular_searches()
            console.input("\nНажмите Enter для возврата в меню...")


        elif choice == "0":
            clear_screen()
            print("До свидания!")
            break

        #console.input("\nНажмите Enter для возврата в меню...")

def show_films_in_pages(films):
    """
    Показывает фильмы порциями по 10 штук.
    Пользователь может запросить следующую страницу
    или вернуться в меню.
    """

    if not films:
        print("\nНичего не найдено.")
        input("\nНажмите Enter для возврата в меню...")
        return

    page_size = 10
    start = 0

    while start < len(films):

        end = start + page_size

        print(
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
            print("\n-=Конец списка.=-")
            input("\nНажмите Enter для возврата в меню...")
            break

        choice = input(
            "\nПоказать следующие 10 фильмов? (Enter — да, 0 — меню): "
        )

        if choice == "0":
            break

        start = end


def show_search_by_keyword():

    keyword = input("\nВведите ключевое слово: ")
    films = get_films_by_keyword(keyword)

    save_search_log(
        search_type="keyword",
        search_params={"keyword": keyword},
        results_count=len(films)
    )

    show_films_in_pages(films)

def show_search_by_category():

    categories = get_categories_with_years()

    if not categories:
        print("\nНичего не найдено.")
    else:

        # for index, item in enumerate(categories, start=1):
        #     print(
        #         f"{index:2}. " # номер занимает 2 символа.
        #         f"{item['category']:<15} " # название жанра выравнивается по левому краю в поле шириной 15 символов
        #         f"({item['first_year']} - {item['last_year']})"
        #     )

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

        choice = int(input("\nВведите номер жанра: ")) # выбор жанра

        selected = categories[choice - 1] # выбранный жанр (словарь!)
        category_id = selected["category_id"]
        category_name = selected["category"]
        first_year = selected["first_year"]
        last_year = selected["last_year"]

        print(f"\nВыбран жанр: {category_name}")
        print(f"Доступные годы: {first_year} - {last_year}")
        year_from = int(
            input(f"\nВведите начальный год ({first_year}-{last_year}): ")
        )

        year_to = int(
            input(f"Введите конечный год ({first_year}-{last_year}): ")
        )

        films = get_films_by_category_id_and_year(
            category_id,
            year_from,
            year_to
        )

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


def format_search_params(item: dict) -> str:
    """
    Формирует строку параметры поискового запроса в кратком виде.

    :param item: словарь с информацией о поисковом запросе.
    :return: строка с параметрами поиска.
    """

    p = item["search_params"]

    if item["search_type"] == "keyword":
        return p["keyword"]

    elif item["search_type"] == "category_name_and_year":
        return f'{p["category_name"]} ({p["year_from"]}-{p["year_to"]})'

    elif item["search_type"] == "category_id_and_year":
        return f'{p["category_id"]} ({p["year_from"]}-{p["year_to"]})'

    return str(p)


def format_search_description(item: dict) -> str:
    """
    Возвращает поисковый запрос в удобном для пользователя виде.
    """

    p = item["search_params"]

    if item["search_type"] == "keyword":
        return f'Ключевое слово: "{p["keyword"]}"'

    elif item["search_type"] == "category_name_and_year":
        return (
            f'Жанр: {p["category_name"]} '
            f'({p["year_from"]}-{p["year_to"]})'
        )

    elif item["search_type"] == "category_id_and_year":
        return (
            f'ID жанра: {p["category_id"]} '
            f'({p["year_from"]}-{p["year_to"]})'
        )

    return str(p)


def show_recent_searches():
    try:
        results_number = int(input("\nВведите желаемое количество запросов: "))
    except ValueError:
        print("Введите целое число.")
        return
    results = get_recent_searches(results_number)

    if not results:
        print("\nНичего не найдено.")
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
    results = get_popular_searches()
    # print(results)

    if not results:
        print("\nНичего не найдено.")
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
