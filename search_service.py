from mysql_connector import (
    get_films_by_keyword,
    get_categories_with_years,
    get_films_by_category_id_and_year,
)


def search_by_keyword(keyword) -> list[dict]:
    """
    Выполняет поиск фильмов по ключевому слову.

    :param keyword: Ключевое слово для поиска.
    :return: Список найденных фильмов.
    """
    return get_films_by_keyword(keyword)


def get_categories() -> list[dict]:
    """
    Возвращает список жанров с диапазоном доступных годов.

    :return: Список жанров.
    """
    return get_categories_with_years()


def search_by_category(category_id, year_from, year_to) -> list[dict]:
    """
    Выполняет поиск фильмов по жанру и диапазону годов.

    :param category_id: ID выбранного жанра.
    :param year_from: Начальный год диапазона.
    :param year_to: Конечный год диапазона.
    :return: Список найденных фильмов.
    """
    return get_films_by_category_id_and_year(
        category_id,
        year_from,
        year_to,
    )
