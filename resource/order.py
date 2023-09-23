import logging

from flask_restful import Resource
from flask import request

from flask_jwt_extended import (jwt_required, get_jwt_identity)
from models.items_model import Item as ItemModel
from schemas.order import OrderSchema
from schemas.order import UsersOrdersSchema
from models.orders_model import ItemsInOrder
from models.orders_model import Order as OrderModel
from models.users_model import User as UserModel
from validators.users_validators import admin_check, rights_check, order_authorization_check

order_scheme = OrderSchema()
order_scheme_list = OrderSchema(many=True)
users_orders_scheme = UsersOrdersSchema
users_orders_scheme_list = UsersOrdersSchema()


class OrdersList(Resource):
    @jwt_required()
    @admin_check
    def get(self):
        admin_id = get_jwt_identity()
        logging.info(f"Aдминистратор с requested_user_id:{admin_id} получил список всех заказов!")
        return {'orders': order_scheme_list.dumps(OrderModel.find_all())}, 200


class Order(Resource):
    @jwt_required()
    def post(cls):
        data = request.get_json()
        items = []
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            logging.error(f"Пользователь c {user_id} не найден!")
            return {"User not found"}, 400
        for item_data in data['items']:
            name = item_data['name']
            count = item_data['qty']
            res = ItemModel.find_by_title(title=name)
            if not res:
                return {"msg": "Item is not present: {}".format(name)}, 404
            current_amount = res.quantity - count
            if current_amount < 0:
                logging.info(f"Товар `{name}` закончился!")
                return {"msg": "We don't have enough. On stock: {}".format(res.quantity)}, 404
            items.append(ItemsInOrder(item_id=ItemModel.find_id(name), quantity=count))

        order = OrderModel(items=items, status="PENDING", user_id=user_id)
        order.save_to_db()

        return order_scheme.dump(order), 201

    @jwt_required()
    @order_authorization_check
    def get(self):
        order_id = request.args['order_id']
        res = OrderModel.find_by_id(order_id)
        if not res:
            logging.error(f"Заказ c order_id:{order_id} не найден!")
            return {"msg": "Order not found"}, 404
        return order_scheme.dump(res), 200

    @jwt_required()
    @admin_check
    def delete(self):
        order_id = request.args['order_id']
        order_check = OrderModel.find_by_id(order_id)
        if order_check:
            order_check.delete_from_db()
            logging.info(f"Товар c order_id: {order_id} удален!")
            return {"msg": "Order successfully deleted"}, 200
        return {"msg": "Order not found"}, 404

    @jwt_required()
    @admin_check
    def put(self):
        data = request.get_json()
        order_id = data['id']
        status = data['status']
        order_check = OrderModel.find_by_id(order_id)
        if order_check:
            order_check.change_status(status)
            order_check.save_to_db()
            logging.info(f"Cтатус товара c order_id: {order_id} изменен!")
            return {"msg": "Order status successfully changed to '{}'".format(status)}, 200
        return {"msg": "Order not found"}, 404


class OrdersOneUser(Resource):
    @jwt_required()
    @rights_check
    def get(self):
        requested_user_id = request.args['requested_user_id']
        orders = OrderModel.find_all_by_user_id(user_id=requested_user_id)
        order_list = [users_orders_scheme_list.dump(order) for order in orders]
        order_details_list = [order.get_order_details() for order in orders]
        if len(order_list) == 0:
            return {'msg': 'Order list is empty'}, 200
        logging.error(f"Получены заказы пользователя с requested_user_id:{requested_user_id}!")
        return {'orders': order_list, 'order_details': order_details_list[0]}

