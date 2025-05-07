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

def create_dependencies(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    client.post('/api/category/create', data=json.dumps({'name': 'Uniforme', 'code': 'UNI'}), content_type='application/json', headers=headers)
    client.post('/api/size/create', data=json.dumps({'name': 'Pequeno', 'abbreviation': 'P'}), content_type='application/json', headers=headers)
    client.post('/api/gender/create', data=json.dumps({'name': 'Masculino', 'abbreviation': 'M'}), content_type='application/json', headers=headers)
    client.post('/api/room/create', data=json.dumps({'name': 'Sala 101', 'shift': 'manhã'}), content_type='application/json', headers=headers)

def test_create_product(client):
    token, _ = get_token(client)
    create_dependencies(client, token)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/api/product/create',
        data=json.dumps({
            'name': 'Uniforme Escolar',
            'description': 'Uniforme completo da escola',
            'category_id': 1,
            'size_id': 1,
            'gender_id': 1,
            'room_id': 1
        }),
        content_type='application/json', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 201 or response.status_code == 200
    data = response.get_json()
    assert 'data' in data or 'message' in data

def test_list_products(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/product/read/all', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data or isinstance(data, list)

def test_read_product_by_id(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    # Dependências
    client.post('/api/category/create', data=json.dumps({'name': 'Uniforme', 'code': 'UNI'}), content_type='application/json', headers=headers)
    client.post('/api/size/create', data=json.dumps({'name': 'Pequeno', 'abbreviation': 'P'}), content_type='application/json', headers=headers)
    client.post('/api/gender/create', data=json.dumps({'name': 'Masculino', 'abbreviation': 'M'}), content_type='application/json', headers=headers)
    client.post('/api/room/create', data=json.dumps({'name': 'Sala 101', 'shift': 'manhã'}), content_type='application/json', headers=headers)
    resp = client.post('/api/product/create', data=json.dumps({'name': 'Uniforme Escolar', 'description': 'Uniforme completo da escola', 'category_id': 1, 'size_id': 1, 'gender_id': 1, 'room_id': 1}), content_type='application/json', headers=headers)
    product_id = resp.get_json()['data']['id']
    response = client.get(f'/api/product/read/{product_id}', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data['id'] == product_id

def test_update_product(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    client.post('/api/category/create', data=json.dumps({'name': 'Uniforme', 'code': 'UNI'}), content_type='application/json', headers=headers)
    client.post('/api/size/create', data=json.dumps({'name': 'Pequeno', 'abbreviation': 'P'}), content_type='application/json', headers=headers)
    client.post('/api/gender/create', data=json.dumps({'name': 'Masculino', 'abbreviation': 'M'}), content_type='application/json', headers=headers)
    client.post('/api/room/create', data=json.dumps({'name': 'Sala 101', 'shift': 'manhã'}), content_type='application/json', headers=headers)
    resp = client.post('/api/product/create', data=json.dumps({'name': 'Uniforme Escolar', 'description': 'Uniforme completo da escola', 'category_id': 1, 'size_id': 1, 'gender_id': 1, 'room_id': 1}), content_type='application/json', headers=headers)
    product_id = resp.get_json()['data']['id']
    response = client.put(f'/api/product/update/{product_id}',
        data=json.dumps({'name': 'Uniforme Atualizado', 'description': 'Novo desc', 'category_id': 1, 'size_id': 1, 'gender_id': 1, 'room_id': 1}),
        content_type='application/json', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data['name'] == 'Uniforme Atualizado'

def test_delete_product(client):
    token, _ = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    client.post('/api/category/create', data=json.dumps({'name': 'Uniforme', 'code': 'UNI'}), content_type='application/json', headers=headers)
    client.post('/api/size/create', data=json.dumps({'name': 'Pequeno', 'abbreviation': 'P'}), content_type='application/json', headers=headers)
    client.post('/api/gender/create', data=json.dumps({'name': 'Masculino', 'abbreviation': 'M'}), content_type='application/json', headers=headers)
    client.post('/api/room/create', data=json.dumps({'name': 'Sala 101', 'shift': 'manhã'}), content_type='application/json', headers=headers)
    resp = client.post('/api/product/create', data=json.dumps({'name': 'Uniforme Escolar', 'description': 'Uniforme completo da escola', 'category_id': 1, 'size_id': 1, 'gender_id': 1, 'room_id': 1}), content_type='application/json', headers=headers)
    product_id = resp.get_json()['data']['id']
    response = client.delete(f'/api/product/delete/{product_id}', headers=headers)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 200
    response = client.get(f'/api/product/read/{product_id}', headers=headers)
    assert response.status_code == 404 