import library.adapters.repository as repo

def get_daily_pick():
    book = repo.repo_instance.get_random_book()
    return book

def get_all_books_alphabetical():
    all_books = repo.repo_instance.get_all_books_alphabetical()
    return all_books

def get_all_books_release_year():
    all_books = repo.repo_instance.get_all_books_release_year()
    return all_books

def get_all_books_average_rating():
    all_books = repo.repo_instance.get_all_books_average_rating()
    return all_books

def get_books_by_author(author_id):
    author_books = repo.repo_instance.get_books_by_author(author_id)
    return author_books

