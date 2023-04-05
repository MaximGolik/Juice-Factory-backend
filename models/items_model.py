from flask import send_from_directory, jsonify

from db import db
from typing import List


class ImagesForItem(db.Model):
    __tablename__ = "images_for_items"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    filename = db.Column(db.String(200), nullable=False)

    item = db.relationship("Item")

    def serve_image(self, upload_folder, filename):
        return send_from_directory(upload_folder, filename)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)

    images = db.relationship("ImagesForItem", back_populates="item", cascade="all,delete")

    # def __init__(self, title, description, price, quantity):
    #     self.title = title
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity

    @classmethod
    def find_by_title(cls, title: str):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, item_id: str):
        return cls.query.filter_by(id=item_id).first()

    # @classmethod
    # def add_image(cls, item_id, picture):
    #     cls.query.filter_by(id = item_id).first()
    #     cls.picture = picture

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def find_id(cls, title: str):
        obj = cls.query.filter_by(title=title).first()
        return obj.id

    def get_images(self) -> List:
        return ImagesForItem.query.filter_by(item_id=self.id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
