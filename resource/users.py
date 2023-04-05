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
        user = User(phone_number, password, first_name, email)
        user.save_to_db()
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
        if not User.check_password(phone_number, password):
            return {"msg": 'Wrong password'}, 400
        if user and User.check_password(phone_number, password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "first_name": user.first_name
            }, 200
        return {"msg": "Wrong credits"}, 400


class UserMakeAdmin(Resource):
    @classmethod
    def put(cls):
        # todo убрать хардкод на тестах
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
        return {'msg', "Admin is added"}, 201


class UserMethods(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id=user_id)
        if not user:
            return {"msg": "User not found"}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {"msg": "User not found"}, 404
        user.delete_from_db()

        return {"msg": "user deleted successfully"}


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {"User not found"}, 401
        new_jwt_token = create_access_token(identity=current_user, fresh=False)
        return {
            "access_token": new_jwt_token
        }


class UserProperties(Resource):
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        user_check = User.find_by_id(user_id)
        if str(user_id) != id:
            if not user_check.isAdmin:
                return {"msg": "Access denied"}, 401
        user = User.find_by_id(id)
        if not user:
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
        return {"msg": "User updated"}, 200
