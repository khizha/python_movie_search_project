from mysql_connector import get_films_by_keyword
from mysql_connector import get_films_by_category_id_and_year
from mysql_connector import get_films_by_category_name_and_year
from mysql_connector import get_years
from mysql_connector import get_categories

from mongo_logger import save_search_log
from mongo_logger import get_popular_searches
from mongo_logger import get_recent_searches

from pprint import pprint
#from tabulate import tabulate  # pip install tabulate

from datetime import datetime

keyword = "gra"
films = get_films_by_keyword(keyword)
save_search_log(
    search_type="keyword",
    search_params={
        "keyword": keyword,
    },
    results_count=len(films),
)


category_id = 1
start_year = 1994
end_year = 2003
films = get_films_by_category_id_and_year(
    category_id,
    start_year,
    end_year
)
save_search_log(
    search_type="category_id_and_year",
    search_params={
        "category_id": category_id,
        "year_from": start_year,
        "year_to": end_year,
    },
    results_count=len(films),
)


category = "Action"
start_year = 1994
end_year = 2003
films = get_films_by_category_name_and_year(
    category,
    start_year,
    end_year
)
save_search_log(
    search_type="category_name_and_year",
    search_params={
        "category_name": category,
        "year_from": start_year,
        "year_to": end_year,
    },
    results_count=len(films),
)


# популярные запросы
pprint(get_popular_searches())
print("*" * 50)

# последние запросы (5 по дефолту)
pprint(get_recent_searches())

#pprint(films)
#print("*" * 50)

# years = get_years()
# pprint(years)
# print("*" * 50)

# categories = get_categories()
# pprint(categories)
# print("*" * 50)