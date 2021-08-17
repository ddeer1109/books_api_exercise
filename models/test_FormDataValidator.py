from datetime import date
from unittest import TestCase

from models.Book import Book
from models.FormDataValidator import FormDataValidator, \
    INVALID_DATE_INFO, \
    INVALID_ISBN_INFO, \
    DUPLICATE_ISBN_INFO, \
    NON_NULL_INFO, \
    INVALID_VALUE_INFO
from Constants import Columns as Col


class TestFormDataValidator(TestCase):

    def setUp(self) -> None:
        self.update_validator_title_pages = FormDataValidator({Col.title: "New title",
                                                               Col.pages_count: "20"}, update_data=True)
        self.update_validator_all = FormDataValidator({
            Col.title: "New title",
            Col.author: "Miller",
            Col.pages_count: "20",
            Col.isbn: "1123123412343",
            Col.publication_date: "2011-01-01"
        }, update_data=True)
        self.update_validator_isbn_short = FormDataValidator({
            Col.title: "New title",
            Col.author: "Miller",
            Col.pages_count: "20",
            Col.isbn: "112312341234",
            Col.publication_date: "2011-01-01"
        }, update_data=True)
        self.update_validator_isbn_long = FormDataValidator({
            Col.title: "New title",
            Col.author: "Miller",
            Col.pages_count: "20",
            Col.isbn: "11231234123411",
            Col.publication_date: "2011-01-01"
        }, update_data=True)
        self.update_validator_isbn_with_letters = FormDataValidator({
            Col.title: "New title",
            Col.author: "Miller",
            Col.pages_count: "20",
            Col.isbn: "1123123g12f41",
            Col.publication_date: "2011-01-01"
        }, update_data=True)
        self.update_validator_isbn_already_in_db = FormDataValidator({
            Col.title: "New title",
            Col.author: "Miller",
            Col.pages_count: "20",
            Col.isbn: Book.query.first().isbn,
            Col.publication_date: "2011-01-01"
        }, update_data=True)
        self.update_validator_date_in_future = FormDataValidator({
            Col.title: "New title",
            Col.author: "Miller",
            Col.pages_count: "20",
            Col.isbn: "1123123412341",
            Col.publication_date: str(date.today().replace(month=date.today().month + 1))  # automate update of date
        }, update_data=True)
        self.add_entry_validator_with_required_values_empty = FormDataValidator({
            Col.title: "",
            Col.pages_count: "20",
            Col.isbn: None
        })
        self.add_entry_validator_with_all_required_fields_correct = FormDataValidator({
            Col.title: "New title",
            Col.author: "Miller",
            Col.pages_count: "20",
            Col.isbn: "1123123412343",
            Col.publication_date: "2011-01-01"
        })
        self.validator_with_pages_count_polluted = FormDataValidator({
            Col.title: "New title",
            Col.author: "Miller",
            Col.pages_count: "20c",
            Col.isbn: "1123123412343",
            Col.publication_date: "2011-01-01"
        })

    def test_validate_insert(self):
        validator_with_all_data_correct = self.add_entry_validator_with_all_required_fields_correct
        self.assertTrue(validator_with_all_data_correct.is_data_valid())

    def test_validate_update(self):
        validator_with_all_data_correct = self.update_validator_all
        self.assertTrue(validator_with_all_data_correct.is_data_valid())

    def test_validate_non_null_fields(self):
        validator_with_empty_fields = self.add_entry_validator_with_required_values_empty
        for column in [Col.title, Col.isbn, Col.author, Col.publication_date]:
            self.assertEqual(validator_with_empty_fields.invalid_fields_info.get(column), NON_NULL_INFO.format(column))

    def test_validate_pages_count(self):
        validator_with_pages_count_polluted = self.validator_with_pages_count_polluted
        self.assertEqual(
            validator_with_pages_count_polluted.invalid_fields_info.get(Col.pages_count),
            INVALID_VALUE_INFO.format(Col.pages_count)
        )

    def test_validate_publication_date(self):
        validator_with_future_date = self.update_validator_date_in_future
        self.assertEqual(validator_with_future_date.invalid_fields_info.get(Col.publication_date), INVALID_DATE_INFO)
        validator_with_past_date = self.update_validator_isbn_short
        self.assertEqual(validator_with_past_date.invalid_fields_info.get(Col.publication_date), None)

    def test_validate_isbn(self):
        validator_with_short_isbn = self.update_validator_isbn_short
        validator_with_long_isbn = self.update_validator_isbn_long
        validator_with_letters_in_isbn = self.update_validator_isbn_with_letters

        validator_with_isbn_already_in_db = self.update_validator_isbn_already_in_db
        duplicated_isbn = validator_with_isbn_already_in_db.form_data.get(Col.isbn)

        self.assertEqual(validator_with_short_isbn.invalid_fields_info.get(Col.isbn), INVALID_ISBN_INFO)
        self.assertEqual(validator_with_long_isbn.invalid_fields_info.get(Col.isbn), INVALID_ISBN_INFO)
        self.assertEqual(validator_with_letters_in_isbn.invalid_fields_info.get(Col.isbn), INVALID_ISBN_INFO)
        self.assertEqual(
            validator_with_isbn_already_in_db.invalid_fields_info.get(Col.isbn),
            DUPLICATE_ISBN_INFO.format(duplicated_isbn)
        )
