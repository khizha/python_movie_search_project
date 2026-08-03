import os

# Align отвечает за выравнивание текста и объектов
from rich.align import Align

# Panel создает рамку вокруг текста
from rich.panel import Panel

from ui_utils import console

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