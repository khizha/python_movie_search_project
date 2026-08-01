import mysql.connector
from local_settings import dbconfig

# список фильмов по ключевому слову
q_get_films_by_keyword = """
    SELECT title, description, release_year
    FROM film
    WHERE title LIKE CONCAT('%', %s, '%'); 
    """

# спиcок фильмов конкретной категории (по имени категории) в указанном промежутке лет
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
    ORDER BY release_year ASC 
    LIMIT 10;
    """

# спиcок фильмов конкретной категории (по id категории) в указанном промежутке лет
q_get_by_category_id_and_year = """
    SELECT title, description, release_year, category_id
    FROM film AS f
    JOIN film_category AS fc
        USING (film_id)
    WHERE category_id = %s
        AND release_year BETWEEN %s AND %s
    ORDER BY release_year ASC 
    LIMIT 10;
    """

# список годов, упорядоченный по возрастанию
q_get_years_list = """
    SELECT DISTINCT release_year
    FROM film
    ORDER BY release_year ASC;
    """

# список жанров фильмов
q_get_categories_list = """
    SELECT name
    FROM category
    ORDER BY name ASC;
    """

#  список "жанр + минимальный год + максимальный год"
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

def connect():
    """
    функция подключения к базе данных
    использует распаковку словаря dbconfig в качестве параметра метода connect
    :return:
    """
    return mysql.connector.connect(**dbconfig)

def execute_query(query, params=()):
    """
    Выполняет SELECT-запрос и возвращает результат.
    """
    connection = None
    cursor = None

    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params)
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Ошибка MySQL: {err}")
        return []

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_films_by_keyword(keyword):
    """ Поиск списка фильмов по ключевому слову"""
    return execute_query(
        q_get_films_by_keyword,
        (keyword,)
    )

def get_films_by_category_id_and_year(category_id, year_from, year_to):
    """
    функция получения списка фильмов по ID жанра и году
    :param category_id:
    :param year_from:
    :param year_to:
    :return:
    """
    return execute_query(
        q_get_by_category_id_and_year,
        (category_id, year_from, year_to)
    )


def get_films_by_category_name_and_year(category_name, year_from, year_to):
    """
    функция получения списка фильмов по имени жанра и году
    :param category_id:
    :param year_from:
    :param year_to:
    :return:
    """
    return execute_query(
        q_get_films_by_category_name_and_years,
        (category_name, year_from, year_to)
    )

def get_years():
    """Функция получения списка годов выпуска фильмов."""
    return execute_query(q_get_years_list)

def get_categories():
    """Функция получения списка жанров фильмов."""
    return execute_query(q_get_categories_list)

def get_categories_with_years():
    """ Поиск списка фильмов по ключевому слову"""
    return execute_query(
        q_get_categories_with_years
    )