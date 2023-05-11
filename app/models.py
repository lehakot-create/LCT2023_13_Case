from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin

from .database import Base


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(64), unique=True)
    password_is_change = Column(Boolean, default=False)
