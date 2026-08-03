import os

from rich.align import Align
from rich.panel import Panel

from ui_utils import console

def clear_screen():
    """
    Очищает экран терминала.
    """
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    """
    Отображает главное меню приложения.
    """

    menu = (
        "1. Поиск по ключевому слову\n"
        "2. Поиск по жанру и диапазону годов выпуска\n"
        "3. Последние запросы\n"
        "4. Популярные запросы\n"
        "\n"
        "0. Выход"
    )

    panel = Panel(
        # Центрируем текст внутри панели
        Align.center(menu),

        title="ПОИСК ФИЛЬМОВ",

        border_style="bright_white",

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