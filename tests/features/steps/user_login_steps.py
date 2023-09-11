import json

from behave import *
from tests.baseclasses.response import Response
from user_models import UserRegister, UserLogin
import requests
import allure


@step('registered user on "{url}"')
def step_impl(context, url):
    for row in context.table:
        with allure.step("Регистрируем пользователь"):
            data = UserRegister(phone_number=row[0], password=row[1], first_name=row[3], email=row[2]).model_dump()
            r = Response(requests.post(url, json=data))
            if not r.assert_status_code(400):
                r.assert_status_code(201)

@step('user login on "{url}"')
def step_impl(context, url):
    for row in context.table:
        with allure.step("Аутентифицируемся пользователем"):
            data = UserLogin(phone_number=row[0], password=row[1]).model_dump()
            context.response = Response(requests.post(url, json=data))


@step('response code is "{code}"')
def step_impl(context, code):
    with allure.step(f"Проверяем соотвествие статус-кода {code}"):
        context.response.assert_status_code(int(code))
