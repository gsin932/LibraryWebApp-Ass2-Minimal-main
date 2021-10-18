import csv
import random

from pathlib import Path

from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository
from library.domain.model import BooksInventory, Book, User, Review, Author

from .jsondatareader import BooksJSONReader


class MemoryRepository(AbstractRepository):


    def __init__(self):
        self.__books = list()
        self.__books_index = {}
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_book(self, book: Book):
        self.__books.append(book)
        self.__books_index[book.title] = book

    def get_number_of_books(self) -> int:
        return len(self.__books)

    def get_book(self, id: int) -> Book:
        return next((book for book in self.__books if book.book_id == id), None)

    def get_all_book_ids(self):
        book_ids = []
        for book in self.__books:

            book_ids.append(book.book_id)
        return book_ids

    def get_random_book(self) -> Book:
        nr_books = self.get_number_of_books()
        if nr_books > 0:
            random_number = random.randint(0, nr_books-1)
            return self.__books[random_number]

        return None

    def get_all_books_alphabetical(self):
        # for book in self.__books:
        #     print(book.authors)
        sorted_books = []
        for book_title in sorted(self.__books_index.keys()):

            sorted_books.append(self.__books_index[book_title])
        return sorted_books

    def get_all_books_release_year(self):
        books_dict = {}
        unknown_year_list = []
        for book in self.__books:

            if book.release_year is None:
                unknown_year_list.append(book)
            else:
                if book.release_year not in books_dict:
                    books_dict[book.release_year] = [book]
                else:
                    books_dict[book.release_year].append(book)

        sorted_books = []
        for book_release_year in reversed(sorted(books_dict.keys())):
            for book in books_dict[book_release_year]:
                sorted_books.append(book)

        for book in unknown_year_list:
            sorted_books.append(book)

        return sorted_books

    def get_all_books_average_rating(self):
        books_dict = {}
        unknown_rating_list = []
        for book in self.__books:
            if book.average_rating is None:
                unknown_rating_list.append(book)
            else:
                if book.release_year not in books_dict:
                    books_dict[book.average_rating] = [book]
                else:
                    books_dict[book.average_rating].append(book)

        sorted_books = []
        for book_average_rating in reversed(sorted(books_dict.keys())):
            for book in books_dict[book_average_rating]:
                sorted_books.append(book)

        for book in unknown_rating_list:
            sorted_books.append(book)

        return sorted_books

    def get_books_by_author(self, author_id:int):
        print(author_id, "author Id")
        author = Author(author_id, "author")
        all_books = self.__books
        author_books = []
        for book in all_books:
            if author in book.authors:
                author_books.append(book)
        return author_books




def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users

def populate(data_path: Path, repo: MemoryRepository):
    print("Populate Called")
    # Load users into the repository.
    users = load_users(data_path, repo)

    books_file_name = 'comic_books_excerpt.json'
    authors_file_name = 'book_authors_excerpt.json'

    path_to_books_file = str(data_path / books_file_name)
    path_to_authors_file = str(data_path / authors_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file)
    reader.read_json_files()

    for book in reader.dataset_of_books:
        repo.add_book(book)
        
    


