from unittest import TestCase

import db_populator
from data_management.BooksDataManager import BooksDataManager
from models.Book import Book
from models.Constants import Columns as c


class TestBooksDataManager(TestCase):
    def setUp(self) -> None:
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
        self.fail()

    def test_update_entry(self):
        self.fail()

    def test_add_entries(self):
        self.fail()
