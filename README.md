## Juice Factory BackEnd
 
 Это BackEnd часть моего пет-проекта, представляющая из себя приложение для продажи соков онлайн.

Оно написанно на *Python* с помощью фреймоворка *Flask* и использует *PostgreSQL* как базу данных. Юнит-тесты осуществляются с помощью *PyTest*

Также в приложении прописаны `Dockerfile` и `docker-compose.yml` для удобной контейнеризации приложения с помощью docker-compose.

Удобный доступ к API осуществим с помощью *Swagger UI* и коллекции в *Postman*

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

Доступ к `Postman` коллекции можно получить с помощью токена: _будет добавлен позже_

## Тестирование

Для приложения уже есть написанные юнит-тесты

**!!! После запусков тестов база данных буде сброшенна, так как (на момент написания) нет выделенной базы данных для тестов !!!**

Чтобы выполнить тесты и получить отчет о покрытии ими кода необходимо ввести в терминал команду:

`pytest --cov --cov-report=html`

Для получения отчета в Allure:
pytest -v -s --alluredir results
allure serve results

HTML отчет можно открыть в браузере, он находится в `htmlcov/index.html`

## Контакты

Email: `makxim582@gmail.com` / `maxlivegame2@yandex.ru`
