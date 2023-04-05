from flask_restful import Resource
from flask import request

from flask_jwt_extended import (jwt_required, get_jwt_identity)
from models.items_model import Item as ItemModel
from schemas.order import OrderSchema
from schemas.order import UsersOrdersSchema
from models.orders_model import ItemsInOrder
from models.orders_model import Order as OrderModel
from models.users_model import User as UserModel

order_scheme = OrderSchema()
order_scheme_list = OrderSchema(many=True)
users_orders_scheme = UsersOrdersSchema
users_orders_scheme_list = UsersOrdersSchema()


class OrdersList(Resource):
    def get(self):
        from models.orders_model import Order
        return {'orders': order_scheme_list.dumps(Order.find_all())}, 200


class Order(Resource):
    @jwt_required()
    def post(cls):
        data = request.get_json()
        items = []
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"User not found"}, 400

        for item_data in data['items']:
            name = item_data['name']
            count = item_data['qty']
            res = ItemModel.find_by_title(title=name)
            if not res:
                return {"msg": "Item not present {}".format(name)}, 404
            items.append(ItemsInOrder(item_id=ItemModel.find_id(name), quantity=count))

        order = OrderModel(items=items, status="PENDING", user_id=user_id)
        order.save_to_db()

        return order_scheme.dump(order)

    @jwt_required()
    def get(self):
        data = request.get_json()
        order_id = data['id']
        res = OrderModel.find_by_id(order_id)
        if not res:
            return {"msg": "Order with id = {} not present ".format(order_id)}, 404
        return {'order': order_scheme.dump(res)}, 200

    @jwt_required()
    def delete(self):
        data = request.get_json()
        order_id = data['id']
        order_check = OrderModel.find_by_id(order_id)
        if order_check:
            order_check.delete_from_db()
            return {"msg": "Order successfully deleted"}
        return {"msg": "Order not found"}, 404

    @jwt_required()
    def put(self):
        data = request.get_json()
        order_id = data['id']
        status = data['status']
        order_check = OrderModel.find_by_id(order_id)
        if order_check:
            order_check.change_status(status)
            order_check.save_to_db()
            return {"msg": "Order status successfully changed to '{}'".format(status)}, 200
        return {"msg": "Order not found"}, 404


class OrdersOneUser(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id=user_id)
        if not user:
            return {"User not found"}, 400
        orders = OrderModel.find_all_by_user_id(user_id=user_id)
        order_list = [users_orders_scheme_list.dump(order) for order in orders]
        order_details_list = [order.get_order_details() for order in orders]
        return {'orders': order_list, 'order_details': order_details_list[0]}

