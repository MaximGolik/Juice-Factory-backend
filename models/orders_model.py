from db import db
from typing import List


class ItemsInOrder(db.Model):
    __tablename__ = "items_in_order"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column("item_id", db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column("order_id", db.Integer, db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("Item")
    order = db.relationship("Order", back_populates="items")

    @classmethod
    def find_order_details(cls, order_id):
        return cls.query.filter_by(order_id=order_id).all()


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.String(12), nullable=True)

    user = db.relationship("User")
    items = db.relationship("ItemsInOrder", back_populates="order", cascade="all,delete")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def comment(self):
        counts = [f'{data.quantity}x {data.item.name}' for data in self.items]
        return ",".join(counts)

    @property
    def amount(self):
        total = int(sum([item_data.item.price * item_data.quantity for item_data in self.items]) * 100)
        return total

    def change_status(self, new_status):
        self.status = new_status

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, order_id):
        return cls.query.filter_by(id=order_id).first()

    @classmethod
    def find_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_order_details(self):
        items_in_order = ItemsInOrder.query.filter_by(order_id=self.id).all()
        order_details = []
        for item in items_in_order:
            item_details = {
                "item_id": item.item_id,
                'order_id': item.order_id,
                "item_title": item.item.title,
                "item_price": item.item.price,
                "quantity": item.quantity
            }
            order_details.append(item_details)
        return order_details






