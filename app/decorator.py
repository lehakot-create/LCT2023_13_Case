from flask import session, redirect, url_for
from functools import wraps

from config import ADMIN_LOGIN


def authorization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('username') != ADMIN_LOGIN:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function
