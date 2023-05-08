import os
from dotenv import load_dotenv

load_dotenv('.env')

CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SALT = os.environ.get('SALT')

ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
