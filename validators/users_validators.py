import logging
from functools import wraps

from flask import g, request
from flask_jwt_extended import get_jwt_identity

from models.orders_model import Order
from models.users_model import User


def admin_check(f):
    """Декоратор, проверящий является ли пользователь админом"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        check_user_id = get_jwt_identity()
        check_user = User.find_by_id(check_user_id)
        if not check_user or not check_user.isAdmin:
            logging.error(f"Пользователь с user_id:{check_user_id} использовал недоступную для него функцию!")
            return {'msg': 'You need to be an admin'}, 403
        return f(*args, **kwargs)
    return decorated_function


def rights_check(f):
    """Декоратор, проверящий является ли пользователь админом или совпадает ли его user_id c user_id в запросе"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        requester_id = get_jwt_identity()
        requested_user_id = request.args['requested_user_id']
        user = User.find_by_id(requested_user_id)
        requester = User.find_by_id(requester_id)
        if not user:
            logging.error(f"Пользователь c user_id: {requested_user_id} не найден")
            return {"msg": "User not found"}, 404
        if requester_id != user.id:
            logging.error(f"ID не совпадают, {requester_id} != {user.id}")
            if not requester.isAdmin:
                logging.error(f"Пользователь с user_id:{requester_id} использовал недоступную для него функцию")
                return {"msg": "You need to be an admin or it should be your profile"}, 403
        return f(*args, **kwargs)
    return decorated_function


def order_authorization_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        requester_id = get_jwt_identity()
        user = User.find_by_id(requester_id)
        order_id = request.args['order_id']
        res = Order.find_by_id(order_id)
        if not res:
            return {"msg": "Order not found"}, 404
        if res.user_id != user.id:
            logging.error(f"Orders user id: {res.user_id} != user.id: {user.id}")
            if not user.isAdmin:
                logging.error(f"Пользователь с user_id:{requester_id} использовал недоступную для него функцию")
                return {"msg": "You need to be an admin or it should be your profile"}, 403
        return f(*args, **kwargs)
    return decorated_function


