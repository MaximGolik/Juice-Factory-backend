import logging

from flask_restful import Resource
from flask import request
from models.items_model import Item as ItemModel
from models.users_model import User
from schemas.item import ItemSchema
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from validators.users_validators import admin_check

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class ItemList(Resource):
    def get(self):
        return item_list_schema.dump(ItemModel.find_all()), 200


class Item(Resource):
    def get(self):
        item_id = request.args['item_id']
        item = ItemModel.find_by_id(item_id)
        if item:
            return item_schema.dump(item)
        logging.error(f"Товар с item_id:{item_id} не найден!")
        return {"msg": "Item not found"}, 404

    @jwt_required()
    @admin_check
    def post(self):
        try:
            item = item_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        try:
            logging.info(f"Новый товар добавлен!")
            item.save_to_db()
        except:
            logging.error(f"Ошибка при добавлении товара")
            return {"msg": "Error occurred"}
        return item_schema.dump(item), 201

    # 204 код не передает сообщение
    @jwt_required()
    @admin_check
    def delete(self):
        item_id = request.args['item_id']
        item = ItemModel.find_by_id(item_id)
        if not item:
            logging.error(f"Товар не найден!")
            return {"msg": "Item not found"}, 404
        logging.info(f"Товар с item_id:{item_id} удален!")
        item.delete_from_db()
        return {}, 204

    @jwt_required()
    @admin_check
    def put(self):
        data = request.get_json()
        item_id = data["id"]
        title = data["title"]
        description = data["description"]
        price = data["price"]
        quantity = data["quantity"]
        item = ItemModel.find_by_id(item_id)
        if not item:
            logging.error(f"Товар не найден!")
            return {"msg": "Item not found"}, 404
        if item:
            item.price = price
            item.title = title
            item.description = description
            item.quantity = quantity
        logging.info(f"Данные о товаре с item_id:{item_id} обновлены!")
        item.save_to_db()

        return item_schema.dump(item), 200
