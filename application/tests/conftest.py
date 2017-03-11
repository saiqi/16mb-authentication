import pytest

from application.app import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app

    from pymongo import MongoClient

    client = MongoClient(app.config['MONGODB_SETTINGS']['host'])
    client.drop_database('test_database')
    client.close()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
