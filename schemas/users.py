from marsh import ma
from models.users_model import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ("password", "role")
        dump_only = ("id", "activated")
        load_instance = True
