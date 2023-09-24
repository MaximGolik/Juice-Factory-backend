import allure
import pytest

from tests.baseclasses.response import Response
from tests.schemas import items_schemas

@allure.feature('Тестирование методов товаров')
@allure.title('Получить все товары')
def test_get_all_items(client, add_item):
    response = Response(client.get('/items-all'))
    assert response.assert_status_code(200)
    # response.validate(items_schemas.ItemsModels)


@allure.feature('Тестирование методов товаров')
@allure.title('Получить товар по его id')
@pytest.mark.parametrize('item_id', [1])
def test_get_item_by_id(client, add_item, item_id):
    assert add_item == 201
    response = Response(client.get('/item?item_id=1'))
    response.assert_status_code(200)
    response.validate(items_schemas.ItemModel)


@allure.feature('Тестирование методов товаров')
@allure.title('Добавить товар')
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
    response = Response(client.post('/item', json=data, headers=headers))
    response.assert_status_code(201)
    response.validate(items_schemas.ItemModel)


@allure.feature('Тестирование методов товаров')
@allure.title('Неудачно добавить товар')
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
    response = Response(client.post('/item', json=data, headers=headers))
    response.assert_status_code(403)


@allure.feature('Тестирование методов товаров')
@allure.title('Обновить информацию о товаре')
@pytest.mark.parametrize('expected_code', [200])
def test_put_item_positive(client, login_as_admin, add_item, expected_code):
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
        'Authorization': 'Bearer ' + admin_access_token
    }
    response = Response(client.put('/item', json=data, headers=headers))
    response.assert_status_code(expected_code)
    response.validate(items_schemas.ItemModel)


@allure.feature('Тестирование методов товаров')
@allure.title('Не обновить информацию о товаре')
@pytest.mark.parametrize('expected_code, expected_message', [(403, {"msg": "You need to be an admin"})])
def test_put_item_negative(client, login_as_user, add_item, expected_code, expected_message):
    access_token = login_as_user

    assert add_item == 201

    data = {
        "id": 1,
        "title": "Отредактированное",
        "price": 400.0,
        "quantity": 5,
        "description": "Просто неплохой апельсиновый сок"
    }
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.put('/item', json=data, headers=headers))
    response.assert_status_code(expected_code)
    response.assert_message(expected_message)


@allure.feature('Тестирование методов товаров')
@allure.title('Удалить товар')
@pytest.mark.parametrize('expected_code', [204])
def test_delete_item_positive(client, login_as_admin, add_item, expected_code):
    admin_access_token = login_as_admin

    assert add_item == 201

    headers = {
        'Authorization': 'Bearer ' + admin_access_token
    }
    response = client.delete('/item?item_id=1', headers=headers)
    assert response.status_code == expected_code


@allure.feature('Тестирование методов товаров')
@allure.title('Не удалить товар')
@pytest.mark.parametrize('expected_code, expected_message', [(403, {"msg": "You need to be an admin"}),
                                                             (404, {"msg": "Item not found"})])
def test_delete_item_negative(client, login_as_admin, login_as_user, add_item, expected_code, expected_message):
    access_token = login_as_user
    if expected_code == 404:
        access_token = login_as_admin

    assert add_item == 201

    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.delete('/item?item_id=1', headers=headers))
    response.assert_status_code(expected_code)
    response.assert_message(expected_message)

    # response = Response(client.delete('/item?item_id=1', headers=headers))
    response = Response(client.delete('/item?item_id=1', headers=headers))
    response.assert_status_code(expected_code)
    response.assert_message(expected_message)



