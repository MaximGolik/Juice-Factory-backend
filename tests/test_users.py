import allure
import pytest

from tests.baseclasses.response import Response
from tests.schemas import users_schemas


@allure.feature('Тестирование методов пользователей')
@allure.title('Регистрация пользователя')
@pytest.mark.parametrize('data, expected_response, expected_code', [
    ({'phone_number': '79874321348', 'password': 'testPassword', 'first_name': 'Alexey', 'email': 'makarov1@gmail.com'}
     , {'msg': "User successfully registered"}
     , 201)
    ,
    ({'phone_number': '79874321349', 'password': 'testPassword', 'first_name': 'Mikhail', 'email': 'luk@mail.ru'}
     , {'msg': "User successfully registered"}
     , 201)
    ,
    ({'phone_number': '79874321349', 'password': 'testPassword', 'first_name': 'Mikhail', 'email': 'luk@mail.ru'}
     , {"msg": "Phone number is already used"}
     , 400)
    ,
    ({'phone_number': '79874321332', 'password': 'testPassword', 'first_name': 'Andrey', 'email': 'iada.mail.ru'}
     , {'msg': "Email is not valid"}
     , 400)
    ,
    ({'phone_number': '7987432133', 'password': 'testPassword', 'first_name': 'Andrey', 'email': 'shortPhone@gmail.com'}
     , {'msg': "Phone number is too short"}
     , 400)
])
def test_register_user(client, data, expected_response, expected_code):
    response = Response(client.post("/register", json=data))
    response.assert_status_code(expected_code)


@allure.feature('Тестирование методов пользователей')
@allure.title('Авторизация пользователя')
@pytest.mark.parametrize('data, expected_code', [
    ({'phone_number': '79877321243', 'password': 'testPassword'},
     200
     )
])
def test_login_user_positive(client, data, expected_code, login_as_user):
    response = Response(client.post('/auth', json=data))
    response.validate(users_schemas.UserAuthModel)
    response.assert_status_code(expected_code)



@allure.feature('Тестирование методов пользователей')
@allure.title('Неудачная авторизация пользователя')
@pytest.mark.parametrize('data, expected_response, expected_code', [
    ({'phone_number': '79874321123', 'password': 'testPassword'},
     {"msg": 'Wrong credits'},
     401
     )
    ,
    ({'phone_number': '79877321243', 'password': 'testPassword1'},
     {"msg": 'Wrong password'},
     401
     )
])
def test_login_user_negative(client, data, expected_response, expected_code, login_as_user):
    response = Response(client.post('/auth', json=data))
    assert response.assert_status_code(expected_code)
    assert response.response_json == expected_response


@allure.feature('Тестирование методов пользователей')
@allure.title('Создание админа')
def test_create_admin(client):
    response = Response(client.post("/user-make-admin"))
    assert response.response_json == {'msg': "Admin is added"}
    response.assert_status_code(201)


@allure.feature('Тестирование методов пользователей')
@allure.title('Удаление пользователя')
@pytest.mark.parametrize('expected_message, expected_code', [({"msg": "User deleted successfully"}, 200)])
def test_delete_user_positive(client, expected_message, expected_code, login_as_admin, login_as_user):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.delete('user?user_id=1', headers=headers))
    assert response.response_json == expected_message
    response.assert_status_code(expected_code)


@allure.feature('Тестирование методов пользователей')
@allure.title('Неудачное удаление пользователя')
@pytest.mark.parametrize('expected_message, expected_code, access_token_type', [
    ({'msg': 'You need to an admin'}, 403, 'user'),
    ({"msg": "User not found"}, 404, 'admin')
])
def test_delete_user_negative(client, expected_message, expected_code, login_as_user, login_as_admin, access_token_type):
        if access_token_type == 'user':
            access_token = login_as_user
        if access_token_type == 'admin':
            access_token = login_as_admin
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = Response(client.delete('user?user_id=99', headers=headers))
        assert response.assert_status_code(expected_code)
        assert response.response_json == expected_message


@allure.feature('Тестирование методов пользователей')
@allure.title('Неудачно получить пользователя')
@pytest.mark.parametrize('expected_message, expected_code', [({"msg": "You need to be an admin"}, 403)
])
def test_get_user_negative(client, expected_code, expected_message, login_as_user):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.get('/user?user_id=1', headers=headers))
    assert response.response_json == expected_message
    assert response.assert_status_code(expected_code)


@allure.feature('Тестирование методов пользователей')
@allure.title('Получить пользователя')
@pytest.mark.parametrize('expected_code', [200])
def test_get_user_positive(client, expected_code, login_as_user, login_as_admin):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.get('/user?user_id=2', headers=headers))
    response.assert_status_code(expected_code)
    response.validate(users_schemas.UserGetModel)


@allure.feature('Тестирование методов пользователей')
@allure.title('Обновить информацию пользователя как админ')
@pytest.mark.parametrize('data, expected_message, expected_code',[
    ({
        "password": "testPassword",
        "first_name": "Alex",
        "email": "updated_email@gmail.com",
        "phone_number": "79788743215",
        "address": "Sevastopol, Bolshaya Morskaya street, 1"},
     {
        "msg": "User updated"
     }, 200)])
def test_put_user_positive_as_admin(client, data, login_as_user, login_as_admin, expected_code, expected_message):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.put('/user?user_id=2', json=data, headers=headers))
    response.assert_status_code(expected_code)
    assert response.response_json == expected_message

@allure.feature('Тестирование методов пользователей')
@allure.title('Обновить информацию пользователя как пользователь')
@pytest.mark.parametrize('data, expected_message, expected_code', [
    ({
        "password": "testPassword",
        "first_name": "John",
        "email": "updated_email1@gmail.com",
        "phone_number": "79788743210",
        "address": "Sevastopol, Bolshaya Morskaya street, 1"},
     {
        "msg": "User updated"
     }, 200)])
def test_put_user_positive_as_user(client, data, login_as_another_user, login_as_user, expected_code, expected_message):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.put('/user?user_id=2', json=data, headers=headers))
    assert response.response_json == expected_message
    assert response.assert_status_code(expected_code)


@allure.feature('Тестирование методов пользователей')
@allure.title('Получить профиль пользователя')
def test_get_user_profile_successful(client, login_as_user):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = Response(client.get('/profile?user_id=1', headers=headers))
    response.assert_status_code(200)
    response.validate(users_schemas.UserProfileModel)
