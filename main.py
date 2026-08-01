# Импортируем основной объект Rich для вывода информации в консоль
from rich.console import Console

# Panel создает рамку вокруг текста
from rich.panel import Panel

# Align отвечает за выравнивание текста и объектов
from rich.align import Align

import os


from mysql_connector import get_films_by_keyword
from mysql_connector import get_categories_with_years

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
        "2. Поиск по жанру\n"
        "3. Список годов\n"
        "4. Список жанров\n"
        "5. Последние запросы\n"
        "6. Популярные запросы\n"
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
        border_style="green",

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
            search_by_keyword()

        elif choice == "2":
            search_by_category()
            #pass

        elif choice == "3":
            #show_years()
            pass

        elif choice == "4":
            #show_categories()
            pass

        elif choice == "0":
            clear_screen()
            print("До свидания!")
            break

        console.input("\nНажмите Enter для возврата в меню...")


def search_by_keyword():

    keyword = input("\nВведите ключевое слово: ")
    films = get_films_by_keyword(keyword)
    if not films:
        print("\nНичего не найдено.")
    else:
        for film in films:
            print(f"{film['title']} ({film['release_year']})")

    #input("\nНажмите Enter для возврата в меню...")

def search_by_category():

    categories = get_categories_with_years()

    if not categories:
        print("\nНичего не найдено.")
    else:

        for item in categories:

              print(f"{item['category']} ({item['first_year']} - {item['last_year']})")

    #input("\nНажмите Enter для возврата в меню...")

if __name__ == "__main__":

    main()

# ======================================================
# Тестирование функций (временный код)
# ======================================================
# from mysql_connector import get_films_by_keyword
# from mysql_connector import get_films_by_category_id_and_year
# from mysql_connector import get_films_by_category_name_and_year
# from mysql_connector import get_years
# from mysql_connector import get_categories
#
# from mongo_logger import save_search_log
# from mongo_logger import get_popular_searches
# from mongo_logger import get_recent_searches
#
# from pprint import pprint
# #from tabulate import tabulate  # pip install tabulate
#
# from datetime import datetime
#
# keyword = "gra"
# films = get_films_by_keyword(keyword)
# save_search_log(
#     search_type="keyword",
#     search_params={
#         "keyword": keyword,
#     },
#     results_count=len(films),
# )
#
#
# category_id = 1
# start_year = 1994
# end_year = 2003
# films = get_films_by_category_id_and_year(
#     category_id,
#     start_year,
#     end_year
# )
# save_search_log(
#     search_type="category_id_and_year",
#     search_params={
#         "category_id": category_id,
#         "year_from": start_year,
#         "year_to": end_year,
#     },
#     results_count=len(films),
# )
#
#
# category = "Action"
# start_year = 1994
# end_year = 2003
# films = get_films_by_category_name_and_year(
#     category,
#     start_year,
#     end_year
# )
# save_search_log(
#     search_type="category_name_and_year",
#     search_params={
#         "category_name": category,
#         "year_from": start_year,
#         "year_to": end_year,
#     },
#     results_count=len(films),
# )
#
#
# # популярные запросы
# pprint(get_popular_searches())
# print("*" * 50)
#
# # последние запросы (5 по дефолту)
# pprint(get_recent_searches())
#
# #pprint(films)
# #print("*" * 50)
#
# # years = get_years()
# # pprint(years)
# # print("*" * 50)
#
# # categories = get_categories()
# # pprint(categories)
# # print("*" * 50)