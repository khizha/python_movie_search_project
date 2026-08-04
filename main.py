from ui_utils import console, wait_for_enter
from search_handlers import (
    show_search_by_keyword,
    show_search_by_category,
)
from menu import clear_screen, show_menu
from history import (
    show_recent_searches,
    show_popular_searches,
)


def main() -> None:
    """
    Запускает основной цикл приложения.

    Показывает меню и вызывает обработчики
    выбранных пользователем действий.
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
            break

        else:
            console.print("\nНекорректный выбор. Попробуйте снова.")
            console.input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":

    main()
