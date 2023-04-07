# отдельной бд под тесты нет, после тестов удаляется основная
import pytest

from app import app
from db import db


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


@pytest.fixture
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
def login_as_admin(client):
    data = {'phone_number': '73432341234', 'password': 'AdminPassword'}
    client.put("/user-make-admin")
    login_response = client.post('/auth', json=data)
    response_data = login_response.json
    assert 'access_token' in response_data
    access_token = response_data['access_token']
    return access_token