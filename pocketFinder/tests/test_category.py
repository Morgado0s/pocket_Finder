import pytest
import sys
import os
import uuid
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
import json
from app_factory import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def get_token(client):
    email = f"admin_{uuid.uuid4()}@teste.com"
    client.post('/api/admin/create',
        data=json.dumps({
            'name': 'Admin Teste',
            'email': email,
            'password': '123456'
        }),
        content_type='application/json')
    login = client.post('/api/admin/login',
        data=json.dumps({
            'email': email,
            'password': '123456'
        }),
        content_type='application/json')
    return login.get_json().get('access_token'), email

def test_create_category(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/api/category/create',
        data=json.dumps({
            'name': 'Uniforme',
            'code': 'UNI'
        }),
        content_type='application/json', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 201 or response.status_code == 200
    data = response.get_json()
    assert 'data' in data or 'message' in data

def test_list_categories(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/category/read/all', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data or isinstance(data, list)

def test_read_category_by_id(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    nome = f"Categoria {uuid.uuid4()}"
    codigo = f"C{uuid.uuid4().hex[:6]}"
    resp = client.post('/api/category/create',
        data=json.dumps({'name': nome, 'code': codigo}),
        content_type='application/json', headers=headers)
    print(resp.status_code)
    print(resp.get_json())
    category_id = resp.get_json()['data']['id']
    response = client.get(f'/api/category/read/{category_id}', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data['id'] == category_id

def test_update_category(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    nome = f"Categoria {uuid.uuid4()}"
    codigo = f"C{uuid.uuid4().hex[:6]}"
    resp = client.post('/api/category/create',
        data=json.dumps({'name': nome, 'code': codigo}),
        content_type='application/json', headers=headers)
    print(resp.status_code)
    print(resp.get_json())
    category_id = resp.get_json()['data']['id']
    response = client.put(f'/api/category/update/{category_id}',
        data=json.dumps({'name': 'Uniforme Atualizado', 'code': 'UNIA'}),
        content_type='application/json', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data['name'] == 'Uniforme Atualizado'

def test_delete_category(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    nome = f"Categoria {uuid.uuid4()}"
    codigo = f"C{uuid.uuid4().hex[:6]}"
    resp = client.post('/api/category/create',
        data=json.dumps({'name': nome, 'code': codigo}),
        content_type='application/json', headers=headers)
    print(resp.status_code)
    print(resp.get_json())
    category_id = resp.get_json()['data']['id']
    response = client.delete(f'/api/category/delete/{category_id}', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 200
    response = client.get(f'/api/category/read/{category_id}', headers=headers)
    assert response.status_code == 404 