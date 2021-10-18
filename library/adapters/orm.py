from sqlalchemy import *
from sqlalchemy.orm import registry

from library.domain import model

metadata = MetaData()
mapper_registry = registry()
mapper = mapper_registry.map_imperatively



publisher = Table('publisher', metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('publisher_name', String(255), unique=True),
                    )

author = Table('author', metadata,
                  Column('author_id', Integer, unique=True, primary_key=True, autoincrement=True),
                  Column('author_full_name', String(255), unique=True),
                    )

book = Table('book', metadata,
                  Column('id', Integer, unique=True, primary_key=True, autoincrement=True),
                  Column('book_id', String(255)),
                  Column('title', String(255)),
                  Column('image_url', String(255)),
                  # Column('publisher', ForeignKey('publisher.id')),
                  # Column('authors', String(255)),
                  Column('release_year', String(255)),
                  Column('description', Text()),
                  Column('ebook', String(255)),
                  Column('url', String(255)),
                  Column('average_rating', String(255))
                    )

review = Table('review', metadata,
                  Column('id', Integer, unique=True, primary_key=True, autoincrement=True),
                  Column('book', ForeignKey('book.book_id')),
                  Column('review_text', String(255), unique=True),
                  Column('rating', Integer)
                    )

user = Table('user', metadata,
                  Column('id', Integer, unique=True, primary_key=True, autoincrement=True),
                  Column('user_name', String(255), unique=True),
                  Column('password', String(255))
                    )

booksinventory = Table('booksinventory', metadata,
                  Column('id', Integer, unique=True, primary_key=True, autoincrement=True),
                    ) 


def map_model_to_tables():
    mapper(model.Publisher, publisher)

    mapper(model.Author, author, properties={
        'author_id': author.columns.author_id,
        'author_full_name': author.columns.author_full_name
    })

    mapper(model.Book, book, properties={
        'book_id': book.columns.book_id,
        'title': book.columns.title,
        'image_url': book.columns.image_url,
        'ebook': book.columns.ebook,
        # 'publisher': book.columns.publisher,
        'description': book.columns.description,
        'url': book.columns.url,
        'average_rating': book.columns.average_rating,
        'release_year': book.columns.release_year,
        # 'authors': book.columns.authors
    })

    mapper(model.Review, review, properties={
        'review_text': review.columns.review_text,
        'rating': review.columns.rating
    })

    mapper(model.User, user, properties={
      'user_name': user.columns.user_name,
      'password': user.columns.password
    })


    