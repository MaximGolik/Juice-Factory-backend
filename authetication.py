from models.users_model import User


def auth(phone_number, password):
    user = User.find_by_phone_number(phone_number)

    if User.check_password(user.password, password):
        return user
    else:
        return None


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
