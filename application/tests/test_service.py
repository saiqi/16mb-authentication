

def test_create_user(client):
    data = {
        'user': 'toto', 
        'password': 'titi',
        'role': 'admin',
        'first_name': 'Toto',
        'last_name': 'Tutu'
    }
    
    result = client.post('/users', data=data)
    
    assert result.status_code == 201