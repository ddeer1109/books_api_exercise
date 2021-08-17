import requests

from models.Book import Book
from util import util


class BooksApiRequest:
    __VOLUMES_LINK = "https://www.googleapis.com/books/v1/volumes"
    __VOLUMES_QUERYING_LINK = "https://www.googleapis.com/books/v1/volumes?q="
    NOT_FOUND = "Unknown"

    headers = {
        'Content-Type': 'application/json',
    }

    title_api = "title"
    author_api = "authors"
    publication_date_api = "publishedDate"
    isbn_api = "industryIdentifiers"
    pages_count_api = "pageCount"
    link_to_cover_page_api = lambda entry: entry.get("imageLinks", {}).get("thumbnail", "Unknown")
    language_api = "language"

    query = ""

    result = None

    def __init__(self, params_dict=None, **kwargs):
        input_data = params_dict if params_dict else kwargs
        for key in input_data:
            self.query += f"{self.query}{key}:{input_data.get(key)}&"

    def build_query_uri(self, request_options=None):
        basic_query = self.__VOLUMES_QUERYING_LINK + self.query
        if request_options:
            options_queries = "".join([f"{key}={request_options.get(key)}&" for key in request_options])
            return basic_query + options_queries

        return basic_query

    def send_request(self, request_options=None):
        uri = self.build_query_uri(request_options)
        books_request = requests.get(uri, headers=self.headers)
        self.result = books_request.json()['items']

    def get_mapped_results(self):
        books = []
        for entry in self.result:
            volume_data = entry.get("volumeInfo")
            book = self.map_json_volume_data_to_book(volume_data)

            if book:
                books.append(book)

        return books

    def map_json_volume_data_to_book(self, volume_data):

        title = \
            volume_data.get(self.title_api, self.NOT_FOUND)
        author = \
            volume_data.get(self.author_api, self.NOT_FOUND)
        published_date = \
            volume_data.get(self.publication_date_api, self.NOT_FOUND)
        pages_count = \
            volume_data.get(self.pages_count_api, self.NOT_FOUND)
        language = \
            volume_data.get(self.language_api, self.NOT_FOUND)

        isbn = self.get_isbn_from_volume_entry(volume_data)
        cover_page_link = BooksApiRequest.link_to_cover_page_api(volume_data)

        if self.NOT_FOUND not in [title, author, published_date, isbn]:
            return Book(
                title=title,
                author=", ".join(author) if len(author) > 1 else "".join(author),
                publication_date=util.parse_date(published_date),
                isbn=isbn,
                link_to_cover_page=cover_page_link,
                pages_count=pages_count,
                language=language
            )

    def get_isbn_from_volume_entry(self, entry):
        identifiers_section = entry.get(self.isbn_api, [])

        find_isbn = lambda identifier: identifier.get("identifier") \
            if identifier.get("type") in ["ISBN_10", "ISBN_13"] else self.NOT_FOUND

        if len(identifiers_section) >= 1:
            first_id = identifiers_section[0]
            isbn = find_isbn(first_id)

            if isbn != self.NOT_FOUND:
                return isbn

            if len(identifiers_section) >= 2:
                second_id = identifiers_section[1]
                isbn = find_isbn(second_id)
                return isbn

        return self.NOT_FOUND
