from marsh import ma
from models.items_model import Item


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        dump_only = ("id",)
        load_instance = True
        include_fk = True
