## Juice Factory BackEnd
 
 Это BackEnd часть моего пет-проекта, представляющая из себя приложение для продажи соков онлайн.
Идея предложения - песочница для написания тестов и авто-тестов

Оно написанно на *Python* с помощью фреймоворка *Flask* и использует *PostgreSQL* как базу данных. Тестирование осуществляются с помощью *PyTest* и *Behave*

Также в приложении прописаны `Dockerfile` и `docker-compose.yml` для удобной контейнеризации приложения с помощью docker-compose.

Удобный доступ к API осуществим благодаря *Swagger UI* 

## Запуск проекта

Чтобы запустить проект необходимо ввести в консоль:

`pip install -r requirements.txt`

А после:

`python app.py`

Если все работает корректно, то доступ к серверу можно будет получить через http://localhost:5000

## Docker контейнер

**!!! Перед выполнением проверить в `config.py` переменную `SQLALCHEMY_DATABASE_URI` и, при необходимости, раскомментировать нужную строку и закомментировать ненужную !!!**

`Pycharm variant: SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5433/flask_store_db"`

`Docker variant: SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db:5432/flask_store_db"`

Для того чтобы обернуть и развернуть приложение в Docker, необходимо поочердно вписать в консоль следующие команды:

`docker-compose build`

`docker-compose up -d`

После следует убедиться что контейнер развернут корректно с помощью команды

`docker-compose ps`

Если все работает корректно, то доступ к серверу можно будет получить через http://localhost:5000

## Swagger UI и Postman

Доступ к `Swagger UI` можно получить через http://localhost:5000/api/docs/#/ сразу после запуска


## Тестирование

Для приложения уже есть написанные `Pytest` и `Behave` тесты, они находятся в папке `tests`

**!!! После тестирования база данных буде сброшенна!**

Чтобы выполнить тесты и получить отчет о покрытии ими кода необходимо ввести в терминал команду:

`pytest --cov --cov-report=html`

HTML отчет можно открыть в браузере, он находится в `htmlcov/index.html`

Для получения отчета в `Allure`:

`pytest -v -s --alluredir results`

`allure serve results`

Для получения результатов тестирования прописанного в `Behave` в `Allure`:

`behave -f allure_behave.formatter:AllureFormatter -o results tests/features/`

`allure serve results`

**Behave и pytest - это два отдельных test runner, поэтому запустить их одновременно - нельзя**

## Контакты

Email: `makxim582@gmail.com` / `maxlivegame2@yandex.ru`
