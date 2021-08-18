"""
Utility module
"""

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


def parse_date(string_input: str):
    """
    Parse string date in format YYYY-MM-DD into datetime.date object.
    Able to handle with only YYYY or YYYY-MM
    :param string_input:
    :return datetime.date:
    """
    if "T" in string_input:
        string_input = string_input.split("T")[0]

    date_elements = list(map(int, string_input.split("-")))

    year = date_elements[YEAR]
    month = date_elements[MONTH] if len(date_elements) >= 2 else 1
    day = date_elements[DAY] if len(date_elements) == 3 else 1

    return date(year, month, day)


def filter_out_empty_dict_entries(dictionary):
    """
    Filters out keys without values
    :param dictionary:
    :return dictionary:
    """
    return dict(filter(lambda pair: pair[1] not in ["", None], dictionary.items()))


def convert_publication_date(dict_data):
    """
    Converts dict_data["publication_date"] to datetime.date object if present or not yet converted
    :param dict_data:
    :return None:
    """
    publication_date = dict_data.get(Columns.publication_date)
    if publication_date not in [None, ""] and type(publication_date) is not date:
        dict_data[Columns.publication_date] = parse_date(dict_data.get(Columns.publication_date))