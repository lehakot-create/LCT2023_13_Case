import os
from dotenv import load_dotenv, find_dotenv

# load_dotenv('.env')
# load_dotenv(find_dotenv())

CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASS')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_PORT = os.environ.get('POSTGRES_PORT')

SQLALCHEMY_DATABASE_URI = \
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SALT = os.environ.get('SALT')

ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
