# отдельной бд под тесты нет, после тестов удаляется основная
import allure
import pytest
from behave import use_fixture, fixture

from app import app
from db import db


@fixture
def client(context, *args, **kwargs):
    app.config['TESTING'] = True
    app.testing = True
    context.client = app.test_client()
    with app.app_context():
        with allure.step("Инициализация БД"):
            with app.app_context():
                db.create_all()
        yield context.client
        with allure.step("Удаление БД"):
            with app.app_context():
                db.session.remove()
                db.drop_all()


def before_feature(context, feature):
    # -- HINT: Recreate a new flaskr client before each feature is executed.
    print('before feature')
    use_fixture(client, context)



