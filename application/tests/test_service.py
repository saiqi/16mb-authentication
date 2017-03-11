import json


def test_create_user(client):
    data = {
        'user': 'toto', 
        'password': 'titi',
        'role': 'admin',
        'first_name': 'Toto',
        'last_name': 'Tutu',
        'email': 'foo@bar.org'
    }
    
    result = client.post('/users', data=data)
    
    assert result.status_code == 201

    user = client.get('/users/toto')

    assert json.loads(user.data.decode('utf-8'))['email'] == 'foo@bar.org'

    result = client.put('/users/toto', data={'role': 'guest'})

    assert result.status_code == 204
    assert json.loads(client.get('/users/toto').data.decode('utf-8'))['role'] == 'guest'

    password = json.loads(user.data.decode('utf-8'))['password_hash']

    result = client.put('/users/toto', data={'password': 'new_titi'})

    assert result.status_code == 204
    assert json.loads(client.get('/users/toto').data.decode('utf-8'))['password_hash'] != password
