import allure
import requests
from behave import *

from tests.baseclasses.response import Response
from tests.features.steps.user_models import UserRegister


@when('we register user on "{url}"')
def step_impl(context, url):
    for row in context.table:
        with allure.step("Регистрируем пользователя"):
            data = UserRegister(phone_number=row[0], password=row[1], first_name=row[3], email=row[2]).model_dump()
            context.response = Response(requests.post(url, json=data))


@then('response code is "{code}"')
def step_impl(context, code):
    with allure.step(f"Проверяем соответствие статус-кода {code}"):
        context.response.assert_status_code(int(code))
