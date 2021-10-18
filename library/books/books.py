from flask import Blueprint, render_template, request, redirect, url_for

import library.utilities.utilities as utilities

# Configure Blueprint.
books_blueprint = Blueprint('books_bp', __name__)

@books_blueprint.route('/alphabetical', methods=['GET'])
def browse_alphabetical():

    all_books = utilities.get_all_books_alphabetical()

    return render_template(
        'books/browse_list_of_books.html',
        books=all_books,
        daily_pick_book=utilities.get_daily_pick()
    )

@books_blueprint.route('/release_year', methods=['GET'])
def browse_release_year():

    all_books = utilities.get_all_books_release_year()

    return render_template(
        'books/browse_list_of_books.html',
        books=all_books,
        daily_pick_book=utilities.get_daily_pick()
    )

@books_blueprint.route('/average_rating', methods=['GET'])
def browse_average_rating():
    all_books = utilities.get_all_books_average_rating()


    return render_template(
        'books/browse_list_of_books.html',
        books=all_books,
        daily_pick_book=utilities.get_daily_pick()
    )

@books_blueprint.route('/browse_author', methods=['GET'])
def browse_author():
    author_id = request.args.get('author')
    print(author_id)
    if author_id is not None:
        author_books = utilities.get_books_by_author(int(author_id))

        return render_template(
            'books/browse_list_of_books.html',
            books=author_books,
            daily_pick_book=utilities.get_daily_pick()
        )
    return redirect('home_bp.home')


