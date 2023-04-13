class BaseConfig(object):
    # main config
    DEBUG = True

    # database config
    ##todo сменить localhost на db и порт 5433 на 5432 перед docker-compose build
    ##pycharm variant
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5433/flask_store_db"
    ##docker variant
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db:5432/flask_store_db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
