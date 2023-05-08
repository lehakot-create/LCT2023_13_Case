from flask import Flask
from flask_login import LoginManager

from .db_query import get_user, get_user_by_id


app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(username):
#     return get_user(username)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


from app import views
