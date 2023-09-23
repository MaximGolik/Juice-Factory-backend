import allure
import pytest

from tests.baseclasses.response import Response


@allure.feature('Тестирование методов заказов')
@allure.title('Неудачно оставить заказ')
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
    response = Response(client.post('/order', json=data, headers=headers))
    assert response.response_json == expected_message
    assert response.assert_status_code(expected_code)


@allure.feature('Тестирование методов заказов')
@allure.title('Оставить заказ')
@pytest.mark.parametrize('data, expected_code', [({'items': [{"name": "Апельсиновый сок", "qty": 1}]}, 201)])
def test_add_order_positive(client, login_as_user, add_item, data, expected_code):
    access_token = login_as_user
    assert add_item == 201
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.post('/order', json=data, headers=headers))
    assert response.assert_status_code(expected_code)


@allure.feature('Тестирование методов заказов')
@allure.title('Получить заказ')
def test_get_add_orders_positive(client, login_as_admin):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.get('/orders-all',headers=headers))
    assert response.assert_status_code(200)


@allure.feature('Тестирование методов заказов')
@allure.title('Получить все заказы')
def test_get_all_orders_negative(client, login_as_user):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.get('/orders-all', headers=headers))
    assert response.response_json == {"msg": "You need to be an admin"}
    assert response.assert_status_code(403)


@allure.feature('Тестирование методов заказов')
@allure.title('Получить заказ')
def test_get_order_positive(client, login_as_user, login_as_admin, login_as_another_user, add_order):
    user_access_token = login_as_user
    admin_access_token = login_as_admin

    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + user_access_token,
        "Content-Type": 'application/json'
    }
    response = Response(client.get('/order?order_id=1', headers=headers))
    assert response.assert_status_code(200)

    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
        "Content-Type": 'application/json'
    }
    response = Response(client.get('/order?order_id=1', headers=headers))
    assert response.assert_status_code(200)


@allure.feature('Тестирование методов заказов')
@allure.title('Не получить заказ, так как он не найден')
@pytest.mark.parametrize('expected_code, expected_message, user_id', [(404, {"msg": "Order not found"}, -1)])
def test_get_order_negative_not_found(client, login_as_admin, add_order, expected_code, expected_message, user_id):
    admin_access_token = login_as_admin

    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
        "Content-Type": 'application/json'
    }

    response = Response(client.get('/order?order_id='+str(user_id), headers=headers))
    assert response.assert_status_code(expected_code)
    assert response.response_json == expected_message


@allure.feature('Тестирование методов заказов')
@allure.title('Не получить заказ, так как нет прав администратора')
@pytest.mark.parametrize('expected_code, expected_message',
                         [(403, {'msg': 'You need to be an admin or it should be your profile'})])
def test_get_order_negative_authorize(client, login_as_another_user, add_order, expected_code, expected_message):
    user_access_token = login_as_another_user

    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + user_access_token
    }

    response = Response(client.get('/order?order_id=1', headers=headers))
    assert response.assert_status_code(expected_code)
    assert response.response_json == expected_message


#todo переписать тест под параметрированный
@allure.feature('Тестирование методов заказов')
@allure.title('Удалить заказ')
def test_delete_order(client, login_as_admin, login_as_user, add_order):
    admin_access_token = login_as_admin
    user_access_token = login_as_user
    assert add_order == 201

    headers = {
        'Authorization': 'Bearer ' + user_access_token,
        "Content-Type": 'application/json'
    }
    response = Response(client.delete('/order?order_id=1', headers=headers))
    assert response.assert_status_code(403)

    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
        'Content-Type': 'application/json'
    }
    response = Response(client.delete('/order?order_id=1', headers=headers))
    assert response.response_json == {'msg': 'Order successfully deleted'}
    assert response.assert_status_code(200)

    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
        'Content-Type': 'application/json'
    }
    response = Response(client.delete('/order?order_id=99', headers=headers))
    assert response.response_json == {"msg": "Order not found"}
    assert response.assert_status_code(404)


#todo переписать тест под параметрированный
@allure.feature('Тестирование методов заказов')
@allure.title('Получить заказы пользователя')
def test_get_user_orders(client, login_as_admin, login_as_user, login_as_another_user, add_order):
    admin_access_token = login_as_admin
    user_access_token = login_as_user

    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
    }
    response = Response(client.get("/users-orders?requested_user_id=1", headers=headers))
    assert response.assert_status_code(200)

    headers = {
        'Authorization': 'Bearer ' + admin_access_token,
    }
    response = Response(client.get("/users-orders?requested_user_id=99", headers=headers))
    assert response.assert_status_code(404)
    assert response.response_json == {'msg': 'User not found'}

    assert add_order == 201
    headers = {
        'Authorization': 'Bearer ' + user_access_token,
    }
    response = Response(client.get("/users-orders?requested_user_id=2", headers=headers))
    assert response.assert_status_code(200)

    another_user_access_token = login_as_another_user
    headers = {
        'Authorization': 'Bearer ' + another_user_access_token,
    }
    response = Response(client.get("/users-orders?requested_user_id=2", headers=headers))
    assert response.assert_status_code(403)
    assert response.response_json == {'msg': "You need to be an admin or it should be your profile"}







