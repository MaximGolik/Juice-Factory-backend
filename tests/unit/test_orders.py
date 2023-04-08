import pytest


@pytest.mark.parametrize('data, expected_code, expected_message', [
        ({'items': [{"name": "Яблочный сок", "qty": 10}]}, 404, {"msg": "Item is not present: Яблочный сок"}),
        ({'items': [{"name": "Апельсиновый сок", "qty": 999}]}, 404, {"msg": "We don't have enough. On stock: 100"})
])
def test_add_order_negative(client, add_item, login_as_user, data, expected_code, expected_message):
    access_token = login_as_user
    assert add_item == 201
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.post('/order', json=data, headers=headers)
    assert response.json == expected_message
    assert response.status_code == expected_code


@pytest.mark.parametrize('data, expected_code', [({'items': [{"name": "Апельсиновый сок", "qty": 1}]}, 201)])
def test_add_order_positive(client, login_as_user, add_item, data, expected_code):
    access_token = login_as_user
    assert add_item == 201
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.post('/order', json=data, headers=headers)
    assert response.status_code == expected_code


def test_get_add_orders_positive(client, login_as_admin):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.get('/orders-all',headers=headers)
    assert response.status_code == 200


def test_get_all_orders_negative(client, login_as_user):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.get('/orders-all', headers=headers)
    assert response.json == {"msg": "You need to be an admin"}
    assert response.status_code == 403


def test_get_order(client, login_as_user, login_as_admin, login_as_another_user, add_order):
    admin_access_token = login_as_admin
    user_access_token = login_as_user
    another_user_access_token = login_as_another_user

    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + user_access_token
    }
    response = client.get('/order?order_id=1', headers=headers)
    assert response.status_code == 200

    response = client.get('/order?order_id=-1', headers=headers)
    assert response.status_code == 404
    assert response.json == {"msg": "Order not found"}

    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + admin_access_token
    }
    response = client.get('/order?order_id=1', headers=headers)
    assert response.status_code == 200

    headers = {
        'Authorization': 'Bearer ' + another_user_access_token
    }
    response = client.get('/order?order_id=1', headers=headers)
    assert response.status_code == 403
    assert response.json == {'msg': "Forbidden"}


def test_delete_order(client, login_as_admin, login_as_user, add_order):
    admin_access_token = login_as_admin
    user_access_token = login_as_user
    assert add_order == 201

    headers = {
        'Authorization': 'Bearer ' + user_access_token,
        "Content-Type": 'application/json'
    }
    response = client.delete('/order?order_id=1', headers=headers)
    assert response.status_code == 403

    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
        'Content-Type': 'application/json'
    }
    response = client.delete('/order?order_id=1', headers=headers)
    assert response.json == {'msg': 'Order successfully deleted'}
    assert response.status_code == 200

    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
        'Content-Type': 'application/json'
    }
    response = client.delete('/order?order_id=99', headers=headers)
    assert response.json == {"msg": "Order not found"}
    assert response.status_code == 404


def test_get_user_orders(client, login_as_admin, login_as_user, login_as_another_user, add_order):
    admin_access_token = login_as_admin
    user_access_token = login_as_user
    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
    }
    response = client.get("/users-orders?user_id=1", headers=headers)
    assert response.status_code == 200

    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
    }
    response = client.get("/users-orders?user_id=99", headers=headers)
    assert response.status_code == 404
    assert response.json == {'msg': 'User not found'}

    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + user_access_token,
    }
    response = client.get("/users-orders?user_id=2", headers=headers)
    assert response.status_code == 200

    another_user_access_token = login_as_another_user
    headers = {
        'Authorization': 'Bearer ' + another_user_access_token,
    }
    response = client.get("/users-orders?user_id=1", headers=headers)
    assert response.json == {'msg': "You need to be an admin"}
    assert response.status_code == 403





