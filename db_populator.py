from datetime import date

from sqlalchemy.exc import IntegrityError

from app import db
from models.Book import Book


def populate():
    db.drop_all()
    db.create_all()
    try:
        book = Book(title="Stary czlowiek i morze",
                    author="Ernest Hemingway",
                    publication_date=date(2000,11,11),
                    isbn="1234-1234-1234-1235",
                    pages_count=150,
                    link_to_cover_page="asd.pl",
                    language="pl")

        book2 = Book(title="Miecz przeznaczenia",
                     author="Andrzej Sapkowski",
                     publication_date=date(1999, 1, 12),
                     isbn="1234-1234-1210",
                     pages_count=111,
                     link_to_cover_page="asd.pl",
                     language="pl")

        book3 = Book(title="Elve's blood",
                     author="Andrzej Sapkowski",
                     publication_date=date(2005, 1, 12),
                     isbn="1234-1234-1258",
                     pages_count=230,
                     link_to_cover_page="asd.pl",
                     language="eng")

        book4 = Book(title="Krew elfów",
                     author="Andrzej Sapkowski",
                     publication_date=date(2002, 1, 12),
                     isbn="1234-1234-1250",
                     pages_count=230,
                     link_to_cover_page="asd.pl",
                     language="pl")

        db.session.add(book)
        db.session.add(book2)
        db.session.add(book3)
        db.session.add(book4)

        db.session.commit()
    except IntegrityError:
        print("already set values")
