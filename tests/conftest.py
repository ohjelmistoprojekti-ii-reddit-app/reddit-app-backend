import pytest
import mongomock
from unittest import mock
from app import create_app
from app.services.db import connect_db

@pytest.fixture
def app():
    """ Creates and returns a Flask application configured for testing """
    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret"
    yield app

@pytest.fixture
def client(app):
    """ Returns a test client for the Flask application, allowing simulation of HTTP requests """
    return app.test_client()

@pytest.fixture
def mock_db(monkeypatch):
    """ Returns a mock database connection by setting a mock connection string and patching MongoClient with mongomock """
    monkeypatch.setenv("ATLAS_CONNECTION_STR", "mongodb://mock")
    with mock.patch("app.services.db.MongoClient") as mock_client_class:
        mock_client = mongomock.MongoClient()
        mock_client_class.return_value = mock_client
        client, db = connect_db()
        yield db