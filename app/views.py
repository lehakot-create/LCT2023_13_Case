from flask import render_template, redirect, session, url_for, request
from flask_login import login_required, login_user

from app import app
from .forms import LoginForm, ChangePassword
from .models import User
from .utils import hash_password
from config import ADMIN_LOGIN, ADMIN_PASSWORD
from .database import db_session


@app.route('/')
@app.route('/index')
@login_required
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html',
                               user=username)
    return render_template('blank.html',
                           user=None,
                           message="You are not logged in")


@app.route('/admin')
@login_required
def admin():
    print('h')
    if 'username' in session:
        username = session['username']
        if username == ADMIN_LOGIN:
            return render_template('admin.html',
                                   user=username)
    return render_template('blank.html',
                           user=None,
                           message='Access is denied')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.name.data).first()
            username = form.name.data
            session['username'] = username
            key = hash_password(form.password.data)

            if username == ADMIN_LOGIN and key == ADMIN_PASSWORD:
                # user = User(name=username,
                #             password=key)
                login_user(user)
                return redirect(url_for('admin'))

            if user is None:
                return render_template('blank.html',
                                       user=None,
                                       message='Encorrect login or password')
            if not user.password_is_change:
                return redirect(url_for('change_password'))

            if user.password == key:
                return redirect(url_for('index'))
            else:
                return render_template('blank.html',
                                       user=None,
                                       message='Encorrect login or password')
    return render_template('login.html',
                           form=form,
                           user=None)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = LoginForm()
    if 'username' in session:
        username = session['username']
        if username == ADMIN_LOGIN:
            if request.method == 'POST':
                if form.validate_on_submit():
                    user = form.name.data
                    key = hash_password(form.password.data)
                    try:
                        new_user = User(
                            name=user,
                            password=key
                        )
                        db_session.add(new_user)
                        db_session.commit()
                    except Exception as e:
                        print(e)
                        return render_template('blank_admin.html',
                                               user=username,
                                               message='Ошибка при создании пользователя')
                    return render_template('blank_admin.html',
                                           user=username,
                                           message='Пользователь успешно создан')
        return render_template('create_user.html',
                               user=username,
                               form=form)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePassword()
    print(session['username'])
    user = User.query.filter_by(name=session['username']).first()
    print(user.name)
    if request.method == 'POST':
        if form.validate_on_submit():

            old_password = form.old_password.data
            if hash_password(old_password) != user.password:
                return render_template('blank.html',
                                       message='Не корректный старый пароль')

            new_password = form.new_password.data
            repeat_new_password = form.repeat_new_password.data
            if new_password != repeat_new_password or new_password is None:
                return render_template('blank.html',
                                       message='Новые пароли не совпадают')
            try:
                user.password = hash_password(new_password)
                user.password_is_change = True
                db_session.add(user)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                print('Пароль уже используется', e)
                return render_template('blank.html',
                                       message='Пароль уже используется. Выберите другой.')
            return render_template('blank.html',
                                   message='Пароль успешно изменен')

    return render_template('change_password.html',
                           form=form)
