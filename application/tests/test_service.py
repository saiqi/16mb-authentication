import json

import pytest

from application.models import User


@pytest.fixture
def admin_user():
    user = User(user_name='admin', email='admin@16mb.org', role='admin')
    user.hash_password('admin')
    user.save()

    yield user

    user.delete()


@pytest.fixture
def read_user():
    user = User(user_name='read', email='read@16mb.org', role='read')
    user.hash_password('read')
    user.save()

    yield user

    user.delete()


def test_create_user(app, admin_user, read_user):
    with app.test_client() as client:
        auth = client.post('/auth', data={'user': 'admin', 'password': 'admin'})

        token = json.loads(auth.data.decode('utf-8'))

        result = client.post('/users', data={'user': 'toto', 'password': 'toto', 'email': 'toto@16mb.org'},
                             headers={'Authorization': token})

        assert result.status_code == 201

        user = client.get('/users/toto', headers={'Authorization': token})

        assert json.loads(user.data.decode('utf-8'))['email'] == 'toto@16mb.org'

        result = client.put('/users/toto', data={'role': 'write'}, headers={'Authorization': token})

        assert result.status_code == 204

        user = client.get('/users/toto', headers={'Authorization': token})

        assert json.loads(user.data.decode('utf-8'))['role'] == 'write'

        password = json.loads(user.data.decode('utf-8'))['password_hash']

        result = client.put('/users/toto', data={'password': 'new_toto'}, headers={'Authorization': token})

        user = client.get('/users/toto', headers={'Authorization': token})

        assert result.status_code == 204
        assert json.loads(user.data.decode('utf-8'))['password_hash'] != password

        auth = client.post('/auth', data={'user': 'read', 'password': 'read'})
        token = json.loads(auth.data.decode('utf-8'))

        result = client.get('/users/toto', headers={'Authorization': token})
        assert result.status_code == 403


def test_authentication(app, admin_user, read_user):
    with app.test_client() as client:
        result = client.post('/auth', data={'user': 'admin', 'password': 'admin'})
        assert result.status_code == 201

        result = client.post('/auth', data={'user': 'admin', 'password': 'tItI'})
        assert result.status_code == 403

        result = client.post('/auth', data={'user': 'nonexisted', 'password': 'tItI'})
        assert result.status_code == 403
