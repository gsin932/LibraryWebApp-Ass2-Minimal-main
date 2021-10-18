import abc

from library.domain.model import User, Book, Review


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        """ Adds a Book to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, id: int) -> Book:
        """ Returns Book with id from the repository.

        If there is no Book with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_random_book(self) -> Book:
        """ Returns a random Book from the repository.

        If there are no Books in the repository, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        """ Returns the number of Books in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books_alphabetical(self):
        """ Returns all books sorted alphabetically by title.

        If there are no Books in the repository, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books_release_year(self):
        """ Returns all books sorted by release year, newest first, unknown release year is at the end.

        If there are no Books in the repository, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books_average_rating(self):
        """ Returns all books sorted by average rating, highest rating first, unknown rating is at the end.

        If there are no Books in the repository, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_book_ids(self):
        """ Returns a list of ids representing Books

        If there are no Books in the repository, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author(self, author_id: int):
        """ Returns a list of books that have have an author with a matching author_id

         If there are no matching books in the repository, this method returns an empty list.
        """
        raise NotImplementedError

