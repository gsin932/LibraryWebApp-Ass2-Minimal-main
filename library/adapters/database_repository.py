from sqlalchemy.orm import scoped_session
from library.domain.model import Book, User, Author
from library.adapters.repository import AbstractRepository
from pathlib import Path
from werkzeug.security import generate_password_hash
import csv
import random
from .jsondatareader import BooksJSONReader

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session =  scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        self.__books_index = {}

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_books(self):
        all_books = []
        try:
            all_books = self._session_cm.session.query(Book).all()
        except Exception:
            print('No article found in DB!')
            pass
        return all_books

    def add_book(self, book: Book):
        self._session_cm.session.add(book)
        self._session_cm.session.commit()
        self.__books_index[book.title] = book
    
    def get_number_of_books(self) -> int:
        books = self.get_books()
        return len(books)

    def get_all_book_ids(self):
        pass

    def get_all_books_alphabetical(self):
        sorted_books = []
        for book_title in sorted(self.__books_index.keys()):
            sorted_books.append(self.__books_index[book_title])
        return sorted_books
    
    def get_all_books_average_rating(self):
        books = self.get_all_books_alphabetical()
        books_dict = {}
        unknown_rating_list = []
        for book in books:
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

    def get_all_books_release_year(self):
        books = self.get_all_books_alphabetical()
        
        books_dict = {}
        unknown_year_list = []
        for book in books:
            print(book, "Book")
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

    def get_book(self):
        pass

    def get_books_by_author(self, author_id):
        author = Author(author_id, "author")
        all_books = self.get_books()
        author_books = []
        for book in all_books:
            if author in book.authors:
                author_books.append(book)
        return author_books

    def get_random_book(self):
        books = self.get_books()
        nr_books = self.get_number_of_books()
        if nr_books > 0:
            random_number = random.randint(0, nr_books-1)
            return books[random_number]

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

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

def load_users(data_path: Path, repo: SqlAlchemyRepository):
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

def populate(data_path: Path, repo: SqlAlchemyRepository):
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



