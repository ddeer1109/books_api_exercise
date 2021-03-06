from datetime import date

from models.Book import Book
from models.Constants import Columns
from util import util

NON_NULL_INFO = "Field {} must not be null"
INVALID_VALUE_INFO = "Field {} has incorrect value"
INVALID_ISBN_INFO = "Field ISBN has incorrect value. Must be 13 or 10 digits separated with - or spaces;"
DUPLICATE_ISBN_INFO = "There is already {} value in DB. Must be unique;"
INVALID_DATE_INFO = "Publication date cannot be in future"

VALID_ISBN_LENGTHS = [10, 13]


class FormDataValidator:
    """
    Class responsible for validating insert or update data from form packed as dictionary.

    Flag update_data set on True:
        - makes content validation only on fields which aren't null and which have specific requirements.
    On false:
        - makes non_null validation on required fields and then content validation as above
    """
    def __init__(self, dict_data, update_data=False) -> None:
        self.form_data = dict_data
        self.is_update_data = update_data
        self.invalid_fields_info = dict()
        self.validate_data()

    def validate_data(self):
        if self.is_update_data:
            self.validate_fields_content()
        else:
            self.validate_insert()

    def validate_insert(self):
        self.validate_non_null_fields()
        self.validate_fields_content()

    def validate_fields_content(self):
        if self.form_data.get(Columns.pages_count):
            self.validate_pages_count()

        if self.form_data.get(Columns.publication_date):
            self.validate_publication_date()

        if self.form_data.get(Columns.isbn):
            self.validate_isbn()

    def is_data_valid(self):
        return len(self.invalid_fields_info) == 0

    def validate_non_null_fields(self):
        for column in [Columns.title, Columns.author, Columns.publication_date, Columns.isbn]:
            if self.form_data.get(column) in ["", None]:
                self.invalid_fields_info[column] = NON_NULL_INFO.format(column)

    def validate_pages_count(self):
        pages_count = self.form_data[Columns.pages_count]

        if not str.isdigit(pages_count) or int(pages_count) <= 0:
            self.invalid_fields_info[Columns.pages_count] = INVALID_VALUE_INFO.format(Columns.pages_count)

    def validate_publication_date(self):

        if util.parse_date(self.form_data[Columns.publication_date]) > date.today():
            self.invalid_fields_info[Columns.publication_date] = INVALID_DATE_INFO

    def validate_isbn(self):
        isbn = self.form_data[Columns.isbn].replace("-", "").replace(" ", "")

        if not (str.isdigit(isbn) and (len(isbn) in VALID_ISBN_LENGTHS)):
            self.invalid_fields_info[Columns.isbn] = INVALID_ISBN_INFO
            return

        if Book.query.filter(
                Book.isbn.like(self.form_data[Columns.isbn])).count() != 0:
            self.invalid_fields_info[Columns.isbn] = DUPLICATE_ISBN_INFO.format(self.form_data[Columns.isbn])
