from flask_restful import Resource
from flask import request
from models.items_model import Item as ItemModel
from models.users_model import User
from schemas.item import ItemSchema
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class ItemList(Resource):
    def get(self):
        return item_list_schema.dump(ItemModel.find_all())


class Item(Resource):
    def get(self):
        item_id = request.args['item_id']
        item = ItemModel.find_by_id(item_id)
        if item:
            return item_schema.dump(item)
        return {"msg": "Item not found"}, 404

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id=user_id)
        if user.isAdmin:
            try:
                item = item_schema.load(request.get_json())
            except ValidationError as err:
                return err.messages, 400
            try:
                item.save_to_db()
            except:
                return {"msg": "Error occurred"}
            return item_schema.dump(item), 201
        return {"msg": "You need to be admin"}, 403

    # 204 код не передает сообщение
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id=user_id)
        if not user.isAdmin:
            return {"msg": "You need to be admin"}, 403
        item_id = request.args['item_id']
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {"msg": "Item not found"}, 404
        item.delete_from_db()
        return {}, 204

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id=user_id)
        if not user.isAdmin:
            return {"msg": "You need to be admin"}, 403
        data = request.get_json()
        item_id = data["id"]
        title = data["title"]
        description = data["description"]
        price = data["price"]
        quantity = data["quantity"]
        item = ItemModel.find_by_id(item_id)
        if item:
            item.price = price
            item.title = title
            item.description = description
            item.quantity = quantity
        else:
            return item.json()

        item.save_to_db()

        return item_schema.dump(item), 200
