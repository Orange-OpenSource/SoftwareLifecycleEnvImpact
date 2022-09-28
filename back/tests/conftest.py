import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from api.server import create_app
from impacts_model.data_model import db as _db

TESTDB = "test.db"
# TESTDB_PATH = "/opt/project/data/{}".format(TESTDB)
# TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH


@pytest.fixture(name="app")
def app(request) -> Flask:
    """Session-wide test `Flask` application."""
    app_fixture = create_app("TEST")

    # Establish an application context before running the tests.
    ctx = app_fixture.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app_fixture


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(name="db")
def db(app, request) -> SQLAlchemy:
    """Session-wide test database."""

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(name="session")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown() -> None:
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
