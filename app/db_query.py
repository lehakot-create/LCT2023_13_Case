from .models import User


def get_user_password(username):
    password = User.query.filter(User.name == username).first()
    return password.password


def get_user(username):
    user = User.query.filter(User.name == username).first()
    return user


def get_user_by_id(user_id):
    user = User.query.filter(User.id == user_id).first()
    return user
