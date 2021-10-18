import pytest

from library.adapters import memory_repository
from library.adapters.memory_repository import MemoryRepository
from library.domain.model import User, Book, Review

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the covid/adapters/data folder!
# tests are written against the csv files in tests
TEST_DATA_PATH = get_project_root() / "library" / "adapters" / "data"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo

def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user

def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_book_count(in_memory_repo):
    number_of_books = in_memory_repo.get_number_of_books()

    # Check that the query returned 20 Books (json objects in the file).
    assert number_of_books == 20

def test_repository_can_add_book(in_memory_repo):
    id = 101
    book = Book(id, "Haensel und Gretel")
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book(id) is book

def test_repository_can_retrieve_book(in_memory_repo):
    existing_book_id = 23272155
    book = in_memory_repo.get_book(existing_book_id)
    assert book.title == "The Breaker New Waves, Vol 11"

def test_repository_does_not_retrieve_a_non_existent_book(in_memory_repo):
    non_existing_book_id = 101
    book = in_memory_repo.get_book(non_existing_book_id)
    assert book is None

def test_repository_get_all_books_sorted_alphabetically(in_memory_repo):
    all_books = in_memory_repo.get_all_books_alphabetical()
    assert all_books[0].title == "20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)"
    assert all_books[4].title == "Crossed + One Hundred, Volume 2 (Crossed +100 #2)"
    assert all_books[7].title == "D.Gray-man, Vol. 16: Blood & Chains"
    assert all_books[15].title == "The Switchblade Mamma"

def test_repository_get_all_books_sorted_release_year(in_memory_repo):
    all_books = in_memory_repo.get_all_books_release_year()
    assert all_books[0].title == "Cruelle"
    assert all_books[0].release_year == 2016
    assert all_books[5].title == "The Breaker New Waves, Vol 11"
    assert all_books[5].release_year == 2014
    assert all_books[15].title == "Superman Archives, Vol. 2"
    assert all_books[15].release_year == 1997

def test_repository_get_all_books_by_average_rating(in_memory_repo):
    all_books = in_memory_repo.get_all_books_average_rating()
    assert all_books[0].title == "D.Gray-man, Vol. 16: Blood & Chains"
    assert all_books[0].average_rating == 4.46
    assert all_books[5].title == "Seiyuu-ka! 12"
    assert all_books[5].average_rating == 4.31
    assert all_books[15].title == "A.I. Revolution, Vol. 1"
    assert all_books[15].average_rating == 3.44

def test_repository_get_books_by_author(in_memory_repo):
    existing_book_id = 23272155
    book = in_memory_repo.get_book(existing_book_id)
    author_id = book.authors[0].unique_id
    books = in_memory_repo.get_books_by_author(author_id)
    assert books[0].title == "The Breaker New Waves, Vol 11"

def test_repository_get_books_by_non_existing_author(in_memory_repo):
    author_id = 1
    books = in_memory_repo.get_books_by_author(author_id)
    assert books == []