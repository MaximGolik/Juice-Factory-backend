import logging
from datetime import datetime

from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import check_password_hash
from flask_login import login_required
from flask_security.confirmable import generate_confirmation_token

from models.users_model import User
from schemas.users import UserSchema
from flask_restful import Resource, reqparse
from flask import request, make_response, render_template, jsonify, flash
from flask_jwt_extended import (create_access_token,
                                create_refresh_token, get_jwt_identity, jwt_required, )
from marshmallow import ValidationError

from validators.users_validators import admin_check, rights_check

user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        first_name = data.first_name
        phone_number = data.phone_number
        password = data.password
        try:
            email_object = validate_email(data.email)
            email = email_object.email
        except EmailNotValidError:
            return {"msg": "Email is not valid"}, 400
        if User.find_by_phone_number(phone_number):
            return {"msg": "Phone number is already used"}, 400
        if User.find_by_email(email):
            return {"msg": "Email is already used"}, 400
        if len(str(phone_number)) < 11:
            return {'msg': 'Phone number is too short'}, 400
        user = User(phone_number, password, first_name, email)
        user.save_to_db()
        logging.info(f"Пользователь с номером телефона {phone_number} зарегистрирован")
        return {'msg': "User successfully registered"}, 201


class UserLogin(Resource):
    def post(self):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        phone_number = data.phone_number
        password = data.password
        user = User.find_by_phone_number(phone_number)
        if not user:
            return {"msg": "Wrong credits"}, 401
        if not User.check_password(phone_number, password):
            return {"msg": 'Wrong password'}, 401
        if user and User.check_password(phone_number, password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            logging.info(f"Пользователь с номером телефона {phone_number} авторизовался")
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "first_name": user.first_name
            }, 200


class UserCreateAdmin(Resource):
    @classmethod
    def post(cls):
        email = "testAdmin@gmail.com"
        password = 'AdminPassword'
        phone_number = '73432341234'
        first_name = 'Admin'
        try:
            email_object = validate_email(email)
            email = email_object.email
        except EmailNotValidError:
            return {"msg": "Email is not valid"}, 400
        if User.find_by_phone_number(phone_number):
            return {"msg": "Phone number already used"}, 400
        if User.find_by_email(email):
            return {"msg": "Email already used"}, 400
        user = User(phone_number, password, first_name, email, isAdmin=True)
        user.save_to_db()
        logging.info("Создан администратор")
        return {'msg': "Admin is added"}, 201


class UserMethods(Resource):
    @classmethod
    @jwt_required()
    @admin_check
    def get(cls):
        user_id = request.args['requested_user_id']
        user = User.find_by_id(user_id)
        if not user:
            logging.error(f"Пользователь с requested_user_id:{user_id} не найден!")
            return {"msg": "User not found"}, 404
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required()
    @admin_check
    def delete(cls):
        user_id = request.args['requested_user_id']
        user = User.find_by_id(user_id)
        if not user:
            logging.error(f"Пользователь с user_id:{user_id} не найден!")
            return {"msg": "User not found"}, 404
        user.delete_from_db()
        logging.info(f"Пользователь с user_id:{user_id} успешно удален!")
        return {"msg": "User deleted successfully"}, 200

    @classmethod
    @jwt_required()
    @rights_check
    def put(cls):
        user_id = request.args['requested_user_id']
        user = User.find_by_id(user_id)
        if not user:
            logging.error(f"Пользователь с user_id:{user_id} не найден!")
            return {"msg": "User not found"}, 404
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=False, location="json")
        parser.add_argument("password", type=str, required=False, location="json")
        parser.add_argument("first_name", type=str, required=False, location="json")
        parser.add_argument("address", type=str, required=False, location="json")
        parser.add_argument("phone_number", type=str, required=False, location="json")
        data = parser.parse_args()
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = data["password"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "address" in data:
            user.address = data["address"]
        if "phone_number" in data:
            user.phone_number = data["phone_number"]
        user.save_to_db()
        logging.info(f"Данные пользователя с requested_user_id:{user_id} успешно изменены!")
        return {"msg": "User updated"}, 200


class ProfileMethods(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        if not user:
            logging.error(f"Пользователь с requested_user_id:{user_id} не найден!")
            return {"msg": "User not found"}, 404
        logging.info(f"Профиль пользователя с requested_user_id:{user_id} успешно получен!")
        return user_schema.dump(user), 200


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        if not current_user:
            logging.error(f"Пользователь с requested_user_id:{current_user} не найден!")
            return {"User not found"}, 401
        new_access_token = create_access_token(identity=current_user, fresh=False)
        new_refresh_token = create_refresh_token(identity=current_user)
        logging.info(f"Refresh token пользователя с requested_user_id:{current_user} успешно создан!")
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
