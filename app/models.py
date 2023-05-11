from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from flask_login import UserMixin

from .database import Base


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(64), unique=True)
    password_is_change = Column(Boolean, default=False)


class ActionLog(Base):
    __tablename__ = 'logging'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    date_time = Column(DateTime, default=datetime.utcnow)
    action = Column(String(50))
