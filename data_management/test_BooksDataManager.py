from unittest import TestCase

from Configuration import Configuration
from app import app

import db_populator
from data_management.BooksDataManager import BooksDataManager
from models.Book import Book
from models.Constants import Columns as c, Status
from util.util import convert_publication_date


class TestBooksDataManager(TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = Configuration.sqlalchemy_test_db
        db_populator.populate()
        self.start_items_count = Book.query.count()

    def test_get_all_books(self):
        self.assertEqual(Book.query.count(), self.start_items_count)
        BooksDataManager.add({
            c.title: "New title",
            c.author: "Miller",
            c.pages_count: "20",
            c.isbn: "1123123412343",
            c.publication_date: "2011-01-01"
        })
        self.assertEqual(Book.query.count(), self.start_items_count+1)

    def test_get_books_by_filters(self):
        self.assertEqual(len(BooksDataManager.get_by_filters(author="Sapkowski")), 3)
        self.assertEqual(len(BooksDataManager.get_by_filters(author="Sapk")), 3)
        self.assertEqual(len(BooksDataManager.get_by_filters(author="sapk")), 3)
        self.assertEqual(len(BooksDataManager.get_by_filters(author="xyza")), 0)

        self.assertEqual(len(BooksDataManager.get_by_filters(published_from="2000-01-01")), 3)
        self.assertEqual(len(BooksDataManager.get_by_filters(published_from="2002-01-01")), 2)
        self.assertEqual(len(BooksDataManager.get_by_filters(published_to="2000-01-01")), 1)

    def test_get_by_id(self):
        book = BooksDataManager.get_by_id(2)
        self.assertEqual(book.title, "Miecz przeznaczenia")
        self.assertEqual(book.author, "Andrzej Sapkowski")
        self.assertEqual(book.isbn, "1234-1234-1210")

        id_not_present_in_db = BooksDataManager.get_by_id(99)
        self.assertIsNone(id_not_present_in_db)

    def test_add_entry(self):
        BooksDataManager.add({
            c.title: "New title",
            c.author: "Miller",
            c.pages_count: "20",
            c.isbn: "1123123412343",
            c.publication_date: "2011-01-01"
        })
        self.assertIsNotNone(BooksDataManager.get_by_filters(title="New title", author="Miller", published_to="2011-01-02"))

    def test_update_entry(self):
        update_data = {
            c.title: "updated title",
            c.author: "",  # this field should not be changed, because is empty
            c.pages_count: "20",
            c.isbn: "1123123412343",
            c.publication_date: "2011-01-01"
        }
        status_should_be_ok = BooksDataManager.update(1, update_data)
        book = BooksDataManager.get_by_id(1)

        self.assertEqual(status_should_be_ok, Status.OK)

        self.assertEqual(book.isbn, update_data[c.isbn])
        self.assertEqual(book.title, update_data[c.title])
        self.assertNotEqual(book.author, update_data[c.author])

        duplicate_isbn = "1234-1234-1210"
        update_data[c.isbn] = duplicate_isbn
        status_should_not_be_ok = BooksDataManager.update(1, update_data)
        self.assertEqual(status_should_not_be_ok, Status.FAILED)

    def test_add_entries(self):
        mock_books = [
            {
                c.title: "New title",
                c.author: "Miller",
                c.pages_count: "20",
                c.isbn: "112312341234-2",
                c.publication_date: "2011-01-01"
            },
            {
                c.title: "New title",
                c.author: "Miller",
                c.pages_count: "20",
                c.isbn: "112312341234-1",
                c.publication_date: "2011-01-01"
            },
            {
                c.title: "New title",
                c.author: "Miller",
                c.pages_count: "20",
                c.isbn: "112312341234-3",
                c.publication_date: "2011-01-01"
            }
        ]
        for book_dict_data in mock_books:
            convert_publication_date(book_dict_data)

        BooksDataManager.add_entries(list(map(Book.build_from_form_dictionary, mock_books)))
        self.assertEqual(Book.query.count(), self.start_items_count + len(mock_books))
