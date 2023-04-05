import enum

from db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from typing import List, Dict, Union

UserJson = Dict[str, Union[int, str]]


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(11), unique=True, nullable=False, index=True)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(30), nullable=True, unique=True)
    address = db.Column(db.String(100), nullable=True)
    isAdmin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)

    def __init__(self, phone_number, password, first_name=None, email=None, active=False, isAdmin = False):
        self.phone_number = phone_number
        self.password = password
        self.first_name = first_name
        self.email = email
        self.isAdmin = isAdmin
        self.active = active

    @classmethod
    def find_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number).first()

    @classmethod
    def check_password(cls, phone_number, password):
        user = cls.query.filter_by(phone_number=phone_number).first()
        return check_password_hash(user.password, password)

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def change_role(cls, user_id):
        cls.query.filter_by(id=user_id).first()
        cls.isAdmin = True
        return cls

    ''' пароль кодируется тут т.к. в __init__ он кодируется ещё раз и далее сравнить
        его с другим паролем уже невозможно'''
    def save_to_db(self):
        db.session.add(self)
        self.password = generate_password_hash(password=self.password).decode('utf-8')
        db.session.commit()

    def update_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()









