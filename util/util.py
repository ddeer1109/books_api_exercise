from datetime import date
from functools import wraps
from flask import jsonify

from models.Constants import Columns

YEAR = 0
MONTH = 1
DAY = 2

def json_response(func):
    """
    Converts the returned dictionary into a JSON response
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return decorated_function


def parse_date(string_input):
    print(string_input)
    date_elements = list(map(int, string_input.split("-")))
    year = date_elements[YEAR]
    month = date_elements[MONTH] if len(date_elements) == 2 else 1
    day = date_elements[DAY] if len(date_elements) == 3 else 1
    return date(year, month, day)


def filter_out_empty_dict_entries(dictionary):
    return dict(filter(lambda pair: pair[1] != "", dictionary.items()))


def convert_publication_date(dict_data):
    if dict_data.get(Columns.publication_date) not in [None, ""]:
        dict_data[Columns.publication_date] = parse_date(dict_data.get(Columns.publication_date))