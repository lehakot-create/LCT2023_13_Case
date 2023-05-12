from .models import User, ActionLog
from .utils import hash_password
from .database import db_session


def get_user_password(username: str):
    password = User.query.filter(User.name == username).first()
    return password.password


def change_user_password(user: User, hash_pass: str):
    user.password = hash_pass
    user.password_is_change = True
    db_session.add(user)
    db_session.commit()


def get_user(username: str):
    user = User.query.filter(User.name == username).first()
    return user


def get_user_by_id(user_id: int):
    user = User.query.filter(User.id == user_id).first()
    return user


def create_admin(login: str, password: str):
    try:
        admin = User(name=login,
                     password=hash_password(password=password))
        db_session.add(admin)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(e)
        print('Администратор уже создан')


def create_new_user(name: str, password: str):
    new_user = User(
                    name=name,
                    password=password
                )
    db_session.add(new_user)
    db_session.commit()


def action_log(username: str, action: str):
    log = ActionLog(name=username,
                    action=action)
    db_session.add(log)
    db_session.commit()
