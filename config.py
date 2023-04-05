import os


class BaseConfig(object):

    # main config
    DEBUG = True
    # WTF_CSRF_ENABLED = True
    # DEBUG_TB_ENABLED = False
    # DEBUG_TB_INTERCEPT_REDIRECTS = False

    # database config

    ##todo сменить localhost на db и порт 5433 на 5432 перед docker-compose build

    ##pycharm variant
    ##SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5433/flask_store_db"

    ##docker variant
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db:5432/flask_store_db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # image upload config
    UPLOAD_FOLDER = "static/images/"
    MAX_CONTENT_PATH = 10 * 1024 * 1024
