from app import db


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String(50))
    publication_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String, unique=True, nullable=False)
    pages_count = db.Column(db.Integer)
    link_to_cover_page = db.Column(db.String)
    language = db.Column(db.String)

    def __repr__(self) -> str:
        return f"""Book: {self.title},
                author: {self.author},
                publication_date: {self.publication_date},
                isbn: {self.isbn},
                pages_count: {self.pages_count},
                link_to_cover_page: {self.link_to_cover_page},
                language: {self.language},
                """


    @staticmethod
    def build_from_form_dictionary(dictionary):

       return Book(
            title=dictionary.get("title"),
            author=dictionary.get("author"),
            publication_date=dictionary.get("publication_date"),
            isbn=dictionary.get("isbn"),
            pages_count=dictionary.get("pages_count"),
            link_to_cover_page=dictionary.get("link_to_cover_page"),
            language=dictionary.get("language"),
    )

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author.split(", "),
            "publication_date": self.publication_date.isoformat(),
            "isbn": self.isbn,
            "pages_count": self.pages_count,
            "link_to_cover_page": self.link_to_cover_page,
            "language": self.language,
        }
