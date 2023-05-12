from flask import Flask
from flask_login import LoginManager

from .db_query import get_user, get_user_by_id, create_admin
from config import ADMIN_LOGIN, ADMIN_PASSWORD
from .models import User


app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def create_administrator():
    create_admin(ADMIN_LOGIN, ADMIN_PASSWORD)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


create_administrator()


from app import views
