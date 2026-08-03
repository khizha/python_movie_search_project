# Импортируем основной объект Rich для вывода информации в консоль
from rich.console import Console

# Создаем объект консоли
# Через него будем выводить все элементы Rich
console = Console()


def wait_for_enter():
    """
    Ожидает нажатия Enter для возврата в меню.
    """
    console.input("\nНажмите Enter для возврата в меню...")