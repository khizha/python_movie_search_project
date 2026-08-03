from ui_utils import console


def get_integer(prompt: str) -> int:
    """
    Запрашивает у пользователя целое число.

    Повторяет запрос, пока не будет введено корректное значение.
    """
    while True:
        try:
            return int(console.input(prompt))

        except ValueError:
            console.print("\nВведите целое число.")


def get_integer_in_range(
    prompt: str,
    min_value: int,
    max_value: int,
    error_message: str | None = None,
) -> int:
    """
    Запрашивает у пользователя целое число
    в заданном диапазоне.
    """
    while True:
        value = get_integer(prompt)

        if min_value <= value <= max_value:
            return value

        if error_message:
            console.print(f"\n{error_message}")
        else:
            console.print(
                f"\nВведите число в диапазоне "
                f"{min_value}–{max_value}."
            )