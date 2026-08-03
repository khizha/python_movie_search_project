# Table создает таблицы
from rich.table import Table
from ui_utils import console, wait_for_enter


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
