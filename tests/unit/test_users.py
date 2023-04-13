import pytest


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
    response = client.post("/register", json=data)
    assert response.json == expected_response
    assert response.status_code == expected_code


@pytest.mark.parametrize('data, expected_code', [
    ({'phone_number': '79874321348', 'password': 'testPassword'},
     200
     )
])
def test_login_user_positive(client, data, expected_code):
    response = client.post('/auth', json=data)
    assert response.status_code == expected_code


@pytest.mark.parametrize('data, expected_response, expected_code', [
    ({'phone_number': '79874321123', 'password': 'testPassword'},
     {"msg": 'Wrong credits'},
     401
     )
    ,
    ({'phone_number': '79874321348', 'password': 'testPassword1'},
     {"msg": 'Wrong password'},
     401
     )
])
def test_login_user_negative(client, data, expected_response, expected_code):
    response = client.post('/auth', json=data)
    assert response.json == expected_response
    assert response.status_code == expected_code


def test_create_admin(client):
    response = client.post("/user-make-admin")
    assert response.status_code == 201
    assert response.json == {'msg': "Admin is added"}


@pytest.mark.parametrize('expected_message, expected_code', [({"msg": "User deleted successfully"}, 200)])
def test_delete_user_positive(client, expected_message, expected_code, login_as_admin):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    delete_response = client.delete('user?user_id=1', headers=headers)
    assert delete_response.json == expected_message
    assert delete_response.status_code == expected_code


@pytest.mark.parametrize('data, expected_message, expected_code', [
    ({'phone_number': '79874321349', 'password': 'testPassword'}, {'msg': 'You need to an admin'}, 403)
    ,
    ({'phone_number': '73432341234', 'password': 'AdminPassword'}, {"msg": "User not found"}, 404)
])
def test_delete_user_negative(client, data, expected_message, expected_code):
    login_response = client.post('/auth', json=data)
    response_data = login_response.json
    assert 'access_token' in response_data
    access_token = response_data['access_token']
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    delete_response = client.delete('user?user_id=99', headers=headers)
    assert delete_response.json == expected_message
    assert delete_response.status_code == expected_code


@pytest.mark.parametrize('expected_message, expected_code', [({"msg": "You need to be an admin"}, 403)
])
def test_get_user_negative(client, expected_code, expected_message, login_as_user):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.get('/user?user_id=1', headers=headers)
    assert response.json == expected_message
    assert response.status_code == expected_code


@pytest.mark.parametrize('expected_code', [200])
def test_get_user_positive(client, expected_code, login_as_admin):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.get('/user?user_id=2 ', headers=headers)
    assert response.status_code == expected_code


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
def test_put_user_positive_as_admin(client, data, login_as_admin, expected_code, expected_message):
    access_token = login_as_admin
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.put('/user?user_id=2', json=data, headers=headers)
    assert response.status_code == expected_code
    assert response.json == expected_message


@pytest.mark.parametrize('data, expected_message, expected_code',[
    ({
        "password": "testPassword",
        "first_name": "John",
        "email": "updated_email1@gmail.com",
        "phone_number": "79788743210",
        "address": "Sevastopol, Bolshaya Morskaya street, 1"},
     {
        "msg": "User updated"
     }, 200)])
def test_put_user_positive_as_user(client, data, login_as_user, expected_code, expected_message):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.put('/user?user_id=2', json=data, headers=headers)
    assert response.json == expected_message
    assert response.status_code == expected_code


def test_get_user_profile_successful(client, login_as_user):
    access_token = login_as_user
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = client.get('/profile?user_id=1', headers=headers)
    assert response.status_code == 200
