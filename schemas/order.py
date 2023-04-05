from marsh import ma
from models.orders_model import Order


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_only = "token"
        dump_only = ("id", "status")
        include_fk = True


class UsersOrdersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_only = ("user_id",)
        dump_only = ('id', 'status')
        include_fk = True
