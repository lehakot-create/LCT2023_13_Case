from flask import render_template, redirect, session, url_for, request
from flask_login import login_required

from app import app
from .forms import LoginForm
from .models import User
from .utils import hash_password
from config import ADMIN_LOGIN, ADMIN_PASSWORD


@app.route('/')
@app.route('/index')
@login_required
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html',
                               title='Home',
                               user=username)
    return "You are not logged in <br><a href = '/login'>" + \
        "click here to log in</a>"


@app.route('/admin')
@login_required
def admin():
    if 'username' in session:
        username = session['username']
        return render_template('admin.html',
                               title='Home',
                               user=username)
    return "You are not logged in <br><a href = '/login'>" + \
        "click here to log in</a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.name.data).first()
            username = form.name.data
            session['username'] = username
            key = hash_password(form.password.data)

            # delete it
            # new_user = User(
            #     name=username,
            #     password=key
            # )
            # db_session.add(new_user)
            # db_session.commit()

            if user is None:
                return 'Encorrect login or password' + '<br>' + \
                    "<b><a href = '/login'>Click here to login</a></b>"

            if user.password == key:
                if username == ADMIN_LOGIN and user.password == ADMIN_PASSWORD:
                    return redirect(url_for('admin'))
                return redirect(url_for('index'))
            else:
                return 'Encorrect login or password' + '<br>' + \
                    "<b><a href = '/login'>Click here to login</a></b>"
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
