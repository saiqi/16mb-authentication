import pytest

from application.app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app()
    yield app

    from pymongo import MongoClient

    client = MongoClient(app.config['MONGODB_SETTINGS']['host'])
    client.drop_database('test_database')
    client.close()
