from ui_utils import console


def get_integer(prompt: str) -> int:
    """
    Запрашивает у пользователя целое число.

    Повторяет запрос до тех пор,
    пока не будет введено корректное значение.

    :param prompt: Текст приглашения ко вводу.
    :return: Введенное пользователем целое число.
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
    в указанном диапазоне.

    Повторяет запрос до получения
    корректного значения.

    :param prompt: Текст приглашения ко вводу.
    :param min_value: Минимально допустимое значение.
    :param max_value: Максимально допустимое значение.
    :param error_message: Сообщение, выводимое при ошибке.
        Если не указано, используется сообщение по умолчанию.
    :return: Введенное пользователем целое число.
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