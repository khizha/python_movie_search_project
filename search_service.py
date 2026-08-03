from mysql_connector import (
    get_films_by_keyword,
    get_categories_with_years,
    get_films_by_category_id_and_year,
)


def search_by_keyword(keyword):
    return get_films_by_keyword(keyword)


def get_categories():
    return get_categories_with_years()


def search_by_category(category_id, year_from, year_to):
    return get_films_by_category_id_and_year(
        category_id,
        year_from,
        year_to,
    )