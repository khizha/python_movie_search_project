from rich.console import Console

console = Console()


def wait_for_enter():
    """
    Ожидает нажатия клавиши Enter.

    Используется перед возвратом
    пользователя в главное меню.
    """
    console.input("\nНажмите Enter для возврата в меню...")
