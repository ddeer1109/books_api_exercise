from models.Book import Book
from sqlalchemy import text


class BookQueryBuilder:
    """
    Builder class which helps to chain different search filters and to return final result.
    """
    def __init__(self) -> None:
        self.query = Book.query


    def filter_by_title(self, title=None):
        self.query = self.query.filter(Book.title.ilike(f"%{title}%")) if title else self.query
        return self

    def filter_by_author(self, author=None):
        self.query = self.query.filter(Book.author.ilike(f"%{author}%")) if author else self.query
        return self

    def filter_by_language(self, language=None):
        self.query = self.query.filter(Book.language.ilike(f"%{language}%")) if language else self.query
        return self

    def filter_by_published_from(self, published_from=None):
        self.query = self.query.filter(text(f"publication_date >= '{published_from}'")) if published_from else self.query
        return self

    def filter_by_published_to(self, published_to=None):
        self.query = self.query.filter(text(f"publication_date <= '{published_to}'")) if published_to else self.query
        return self

    def get_results(self):
        return self.query.all()

