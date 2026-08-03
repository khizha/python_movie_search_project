import mysql.connector
from local_settings import dbconfig

# Поиск фильмов по ключевому слову
q_get_films_by_keyword = """
    SELECT title, description, release_year
    FROM film
    WHERE title LIKE CONCAT('%', %s, '%') 
    ORDER BY title;
    """

# Поиск фильмов по названию жанра в указанном диапазоне лет
q_get_films_by_category_name_and_years = """
    SELECT f.title, 
        f.description, 
        f.release_year, 
        c.name AS category
    FROM film AS f
    JOIN film_category AS fc
        ON f.film_id = fc.film_id
    JOIN category AS c
        ON fc.category_id = c.category_id
    WHERE c.name = %s
        AND f.release_year BETWEEN %s AND %s
    ORDER BY title;
    """

# Поиск фильмов по ID жанра в указанном диапазоне лет
q_get_by_category_id_and_year = """
    SELECT title, description, release_year, category_id
    FROM film AS f
    JOIN film_category AS fc
        USING (film_id)
    WHERE category_id = %s
        AND release_year BETWEEN %s AND %s
    ORDER BY title;    
    """

# Список годов выпуска фильмов
q_get_years_list = """
    SELECT DISTINCT release_year
    FROM film
    ORDER BY release_year ASC;
    """

# Список жанров
q_get_categories_list = """
    SELECT name
    FROM category
    ORDER BY name ASC;
    """

#  Список жанров с минимальным и максимальным годом выпуска фильмов
q_get_categories_with_years = """
    SELECT
        c.category_id,
        c.name AS category,
        MIN(f.release_year) AS first_year,
        MAX(f.release_year) AS last_year
    FROM category AS c
    JOIN film_category AS fc
        ON c.category_id = fc.category_id
    JOIN film AS f
        ON fc.film_id = f.film_id
    GROUP BY c.category_id, c.name
    ORDER BY c.name ASC;
"""

def connect() -> mysql.connector.MySQLConnection:
    """
    Создает подключение к базе данных MySQL.

    Использует параметры подключения,
    указанные в словаре dbconfig.

    :return: Объект подключения MySQL.
    """
    return mysql.connector.connect(**dbconfig)


def execute_query(query, params=()):
    """
    Выполняет SELECT-запрос к базе данных.

    Создает подключение, выполняет запрос
    с указанными параметрами и возвращает
    результат в виде списка словарей.

    :param query: SQL-запрос.
    :param params: Параметры SQL-запроса.
    :return: Список строк результата.
    """
    connection = None
    cursor = None

    # Закрываем соединение и курсор после выполнения запроса
    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_films_by_keyword(keyword):
    """
    Возвращает список фильмов,
    название которых содержит указанное ключевое слово.

    :param keyword: Ключевое слово для поиска.
    :return: Список найденных фильмов.
    """
    return execute_query(
        q_get_films_by_keyword,
        (keyword,)
    )


def get_films_by_category_id_and_year(category_id, year_from, year_to):
    """
    Возвращает список фильмов выбранного жанра
    за указанный диапазон лет.

    :param category_id: Идентификатор жанра.
    :param year_from: Начальный год.
    :param year_to: Конечный год.
    :return: Список найденных фильмов.
    """
    return execute_query(
        q_get_by_category_id_and_year,
        (category_id, year_from, year_to)
    )


def get_films_by_category_name_and_year(category_name, year_from, year_to):
    """
    Возвращает список фильмов выбранного жанра
    за указанный диапазон лет.

    :param category_name: Название жанра.
    :param year_from: Начальный год.
    :param year_to: Конечный год.
    :return: Список найденных фильмов.
    """
    return execute_query(
        q_get_films_by_category_name_and_years,
        (category_name, year_from, year_to)
    )


def get_years():
    """
    Возвращает список годов выпуска фильмов.

    :return: Список годов.
    """
    return execute_query(q_get_years_list)


def get_categories():
    """
    Возвращает список жанров.

    :return: Список жанров.
    """
    return execute_query(q_get_categories_list)


def get_categories_with_years():
    """
    Возвращает список жанров
    с минимальным и максимальным годом выпуска фильмов.

    :return: Список жанров с диапазоном годов.
    """
    return execute_query(
        q_get_categories_with_years
    )