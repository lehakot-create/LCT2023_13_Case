from .models import User
from .utils import hash_password
from .database import db_session


def get_user_password(username):
    password = User.query.filter(User.name == username).first()
    return password.password


def get_user(username):
    user = User.query.filter(User.name == username).first()
    return user


def get_user_by_id(user_id):
    user = User.query.filter(User.id == user_id).first()
    return user


def create_admin(login, password):
    try:
        admin = User(name=login,
                     password=hash_password(password=password))
        db_session.add(admin)
        db_session.commit()
    except Exception as e:
        print(e)
        print('Администратор уже создан')
