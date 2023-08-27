# отдельной бд под тесты нет, после тестов удаляется основная
import allure
import pytest

from app import app
from db import db


@pytest.fixture(scope="module")
@allure.title('База данных')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with allure.step("Инициализация БД"):
            with app.app_context():
                db.create_all()
        yield client
        with allure.step("Удаление БД"):
            with app.app_context():
                db.session.remove()
                db.drop_all()


@pytest.fixture()
@allure.title('Авторизоваться как пользователь №1')
def login_as_user(client):
    data_login = {'phone_number': '79877321243', 'password': 'testPassword'}
    login_response = client.post('/auth', json=data_login)
    response_data = login_response.json
    if not 'access_token' in response_data:
        data_registration = {
            'phone_number': '79877321243',
            'password': 'testPassword',
            "first_name": "Александр",
            "email": "testEmail1@gmail.com"
        }
        client.post("/register", json=data_registration)
        login_response = client.post('/auth', json=data_login)
        response_data = login_response.json
        assert 'access_token' in response_data
    access_token = response_data['access_token']
    return access_token


@pytest.fixture
@allure.title('Авторизоваться как пользователь №2')
def login_as_another_user(client):
    data_login = {'phone_number': '79877321111', 'password': 'testPassword'}
    login_response = client.post('/auth', json=data_login)
    response_data = login_response.json
    if not 'access_token' in response_data:
        data_registration = {
            'phone_number': '79877321111',
            'password': 'testPassword',
            "first_name": "Another Александр",
            "email": "anotherEmail@gmail.com"
        }
        client.post("/register", json=data_registration)
        login_response = client.post('/auth', json=data_login)
        response_data = login_response.json
        assert 'access_token' in response_data
    access_token = response_data['access_token']
    return access_token


@allure.title('Авторизоваться как администратор')
@pytest.fixture
def login_as_admin(client):
    data = {'phone_number': '73432341234', 'password': 'AdminPassword'}
    client.post("/user-make-admin")
    login_response = client.post('/auth', json=data)
    response_data = login_response.json
    assert 'access_token' in response_data
    access_token = response_data['access_token']
    return access_token


@pytest.fixture()
@allure.title('Добавить товар')
def add_item(client, login_as_admin):
    data = {
        "title": "Апельсиновый сок",
        "description": "Просто неплохой апельсиновый сок",
        "price": 130,
        "quantity": 100
    }
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.post('/item', json=data, headers=headers)
    return response.status_code


@allure.title('Добавить заказ')
@pytest.fixture()
def add_order(client, login_as_user, add_item):
    data = {'items': [{"name": "Апельсиновый сок", "qty": 1}]}
    user_access_token = login_as_user
    assert add_item == 201
    headers = {
        'Authorization': 'Bearer ' + user_access_token
    }
    response = client.post('/order', json=data, headers=headers)
    assert response.status_code == 201
    return response.status_code

