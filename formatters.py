def format_search_params(item: dict) -> str:
    """
    Формирует строку параметры поискового запроса в кратком виде.

    :param item: словарь с информацией о поисковом запросе.
    :return: строка с параметрами поиска.
    """

    p = item["search_params"]

    if item["search_type"] == "keyword":
        return p["keyword"]

    elif item["search_type"] == "category_name_and_year":
        return f'{p["category_name"]} ({p["year_from"]}-{p["year_to"]})'

    elif item["search_type"] == "category_id_and_year":
        return f'{p["category_id"]} ({p["year_from"]}-{p["year_to"]})'

    return str(p)


def format_search_description(item: dict) -> str:
    """
    Возвращает поисковый запрос в удобном для пользователя виде.
    """

    p = item["search_params"]

    if item["search_type"] == "keyword":
        return f'Ключевое слово: "{p["keyword"]}"'

    elif item["search_type"] == "category_name_and_year":
        return (
            f'Жанр: {p["category_name"]} '
            f'({p["year_from"]}-{p["year_to"]})'
        )

    elif item["search_type"] == "category_id_and_year":
        return (
            f'ID жанра: {p["category_id"]} '
            f'({p["year_from"]}-{p["year_to"]})'
        )

    return str(p)