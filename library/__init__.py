"""Initialize Flask app."""

from pathlib import Path

from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate
from library.adapters.orm import metadata, map_model_to_tables
from library.adapters import database_repository

REPOSITORY = 'database'
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_ECHO = False
def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('library') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
    if REPOSITORY == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        # fill the content of the repository from the provided json and csv files
        database_mode = False
        populate(data_path, repo.repo_instance)

    elif REPOSITORY == 'database':
        database_uri = SQLALCHEMY_DATABASE_URI
        database_echo = SQLALCHEMY_ECHO

        # Create Database Engine.
        database_engine = create_engine(database_uri, connect_args={'check_same_thread': False}, poolclass=NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)


        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("Repopulating Database")

            clear_mappers()
            metadata.create_all(database_engine) #Coditionally create database tables.
            print("57")
            for table in reversed(metadata.sorted_tables()): #Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate Mappings that map domain model classes to the database tables.

            map_model_to_tables()
            database_repository.populate(data_path, repo.repo_instance)
            database_mode = True
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables
            map_model_to_tables()   
            database_repository.populate(data_path, repo.repo_instance)
            #  Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .books import books
        app.register_blueprint(books.books_blueprint)

    return app
