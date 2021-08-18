from datetime import date

import sqlalchemy

from data_management.BookQueryBuilder import BookQueryBuilder
from models.Book import Book

from app import db
from util import util


class BooksDataManager:

    @staticmethod
    def get_all():
        return Book.query.all()

    @staticmethod
    def get_by_filters(title=None, author=None, language=None, published_from=None, published_to=None):
        results = BookQueryBuilder()\
            .filter_by_title(title)\
            .filter_by_author(author)\
            .filter_by_language(language)\
            .filter_by_published_from(published_from)\
            .filter_by_published_to(published_to)\
            .get_results()

        return results

    @staticmethod
    def get_by_id(id):
        return Book.query.filter(Book.id == id).first()

    @staticmethod
    def add(dict_data):
        util.convert_publication_date(dict_data)
        book = Book.build_from_form_dictionary(dict_data)
        db.session.add(book)
        db.session.commit()

    @staticmethod
    def update(id, dict_data):
        util.convert_publication_date(dict_data)
        cleared = util.filter_out_empty_dict_entries(dict_data)
        try:
            Book.query.filter(Book.id == id).update(cleared)
            db.session.commit()
            return 1
        except sqlalchemy.exc.IntegrityError:
            return -1

    @staticmethod
    def add_entries(books_list):
        for book in books_list:
            try:
                db.session.add(book)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                db.session.registry.clear()
