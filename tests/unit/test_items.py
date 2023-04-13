import pytest


def test_get_all_items(client):
    response = client.get('/items-all')
    assert response.status_code == 200


@pytest.mark.parametrize('item_id', [1])
def test_get_item_by_id(client, add_item, item_id):
    # response_negative = client.get('/item?item_id=1')
    # assert response_negative.status_code == 404
    # assert response_negative.json == {"msg": "Item not found"}

    assert add_item == 201
    response_positive = client.get('/item?item_id=1')
    assert response_positive.status_code == 200


@pytest.mark.parametrize('data', [{
        "title": "Апельсиновый сок",
        "price": 130.0,
        "quantity": 100,
        "description": "Просто неплохой апельсиновый сок"
}])
def test_post_item_positive(client, login_as_admin, data):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.post('/item', json=data, headers=headers)
    assert response.status_code == 201


@pytest.mark.parametrize('data', [{
        "title": "Апельсиновый сок",
        "price": 130.0,
        "quantity": 100,
        "description": "Просто неплохой апельсиновый сок"
}])
def test_post_item_negative(client, login_as_user, data):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.post('/item', json=data, headers=headers)
    assert response.status_code == 403


def test_put_item(client, login_as_user, login_as_admin, add_item):
    user_access_token = login_as_user
    admin_access_token = login_as_admin

    assert add_item == 201

    data = {
        "id": 1,
        "title": "Отредактированное",
        "price": 400.0,
        "quantity": 5,
        "description": "Просто неплохой апельсиновый сок"
    }
    headers = {
        'Authorization': 'Bearer ' + user_access_token
    }
    response = client.put('/item', json=data, headers=headers)
    assert response.status_code == 403
    assert response.json == {"msg": "You need to be admin"}

    headers = {
        'Authorization': 'Bearer ' + admin_access_token
    }
    response = client.put('/item', json=data, headers=headers)
    assert response.status_code == 200


def test_delete_item(client, login_as_user, login_as_admin, add_item):
    user_access_token = login_as_user
    admin_access_token = login_as_admin

    assert add_item == 201

    headers = {
        'Authorization': 'Bearer ' + user_access_token
    }
    response = client.delete('/item?item_id=1', headers=headers)
    assert response.status_code == 403
    assert response.json == {"msg": "You need to be admin"}

    headers = {
        'Authorization': 'Bearer ' + admin_access_token
    }
    response = client.delete('/item?item_id=1', headers=headers)
    assert response.status_code == 204

    response = client.delete('/item?item_id=1', headers=headers)
    assert response.status_code == 404
    assert response.json == {"msg": "Item not found"}



