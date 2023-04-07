from flask import Flask, jsonify, request, send_from_directory
import flask_bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
import os.path

from jwt import ExpiredSignatureError
from werkzeug.utils import secure_filename
from config import BaseConfig

from resource.images import Images
from resource.users import UserRegister, UserMethods, UserLogin, RefreshToken, \
    UserCreateAdmin, ProfileMethods
from resource.items import Item, ItemList
from resource.order import Order, OrdersList, OrdersOneUser
from db import db


from marsh import ma

app = Flask(__name__)
app.secret_key = "pinku"
api = Api(app)
app.config.from_object(BaseConfig())

ALLOWED_EXTENSIONS = {"jpg", "png", "bmp", "jpeg"}

db.init_app(app)
with app.app_context():
    db.create_all()

jwt = JWTManager(app)
bcrypt = flask_bcrypt.Bcrypt(app)
mail = Mail(app)
CORS(app)


@app.errorhandler(ExpiredSignatureError)
def handle_expired_token_error(error):
    return jsonify({'message': 'Your token has expired'}), 401


app.register_error_handler(ExpiredSignatureError, handle_expired_token_error)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": "The token has expired",
        "error": "token_expired"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Signature Invalid",
        "error": "invalid_token"
    }), 401


@jwt.unauthorized_loader
def unauthorized_token(error):
    return jsonify({
        "description": "jwt token not found",
        "error": "token_missing"
    }), 401


@jwt.needs_fresh_token_loader
def fresh_token_loader():
    return jsonify({
        "description": "Require fresh token",
        "error": "fresh_token_required"
    }), 401


@jwt.revoked_token_loader
def revoked_token():
    return jsonify({
        "description": "Token has been revoked",
        "error": "token_revoked"
    }), 401


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


api.add_resource(Item, "/item")
api.add_resource(ItemList, "/items-all")
api.add_resource(UserRegister, "/register")
api.add_resource(UserMethods, "/user")
api.add_resource(UserCreateAdmin, "/user-make-admin")
api.add_resource(UserLogin, "/auth")
api.add_resource(RefreshToken, "/refresh")
api.add_resource(Order, "/order")
api.add_resource(Images, "/image-upload")
api.add_resource(OrdersOneUser, '/users-orders')
# todo переписать фронт под метод с /profile
api.add_resource(ProfileMethods, '/profile')

if __name__ == '__main__':
    api.init_app(app)
    ma.init_app(app)
    db.init_app(app)

    app.run(debug=True, host="0.0.0.0")
