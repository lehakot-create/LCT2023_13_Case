from flask import render_template, redirect, session, url_for, request
from flask_login import login_required, login_user

from app import app
from .forms import LoginForm, ChangePassword
from .models import User, ActionLog
from .utils import hash_password
from config import ADMIN_LOGIN, ADMIN_PASSWORD
from .database import db_session
from .db_query import action_log


@app.route('/')
@app.route('/index')
@login_required
def index():
    if 'username' in session:
        username = session['username']
        action_log(session.get('username', None), 'success log')
        return render_template('index.html',
                               user=username)
    action_log('Anonymous', 'try log')
    return render_template('blank.html',
                           user=None,
                           message="You are not logged in")


@app.route('/admin')
@login_required
def admin():
    if 'username' in session:
        username = session['username']
        if username == ADMIN_LOGIN:
            action_log(username, 'log to admin panel')
            return render_template('admin.html',
                                   user=username)
    action_log('Anonymous', 'try log to admin panel')
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
                action_log(session.get('username', None), 'error login')
                return render_template('blank.html',
                                       user=None,
                                       message='Encorrect login or password')
            if not user.password_is_change:
                return redirect(url_for('change_password'))

            if user.password == key:
                action_log(session.get('username', None), 'success login')
                return redirect(url_for('index'))
            else:
                action_log(session.get('username', None), 'error login')
                return render_template('blank.html',
                                       user=None,
                                       message='Encorrect login or password')
    action_log(session.get('username', None), 'try login')
    return render_template('login.html',
                           form=form,
                           user=None)


@app.route('/logout')
def logout():
    action_log(session['username'], 'log out')
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    action_log(session.get('username', None), 'try create user')
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
                        db_session.rollback()
                        print(e)
                        action_log(session.get('username', None), 'error create user')
                        return render_template('blank_admin.html',
                                               user=username,
                                               message='Ошибка при создании пользователя')
                    action_log(session.get('username', None), 'success create user')
                    return render_template('blank_admin.html',
                                           user=username,
                                           message='Пользователь успешно создан')
        return render_template('create_user.html',
                               user=username,
                               form=form)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    action_log(session.get('username', None), 'try change password')
    form = ChangePassword()
    user = User.query.filter_by(name=session['username']).first()
    if request.method == 'POST':
        if form.validate_on_submit():

            old_password = form.old_password.data
            if hash_password(old_password) != user.password:
                action_log(session.get('username', None), 'error change password')
                return render_template('blank.html',
                                       message='Не корректный старый пароль')

            new_password = form.new_password.data
            repeat_new_password = form.repeat_new_password.data
            if new_password != repeat_new_password or new_password is None:
                action_log(session.get('username', None), 'error change password')
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
                action_log(session.get('username', None), 'error change password')
                return render_template('blank.html',
                                       message='Пароль уже используется. Выберите другой.')
            action_log(session.get('username', None), 'success change password')
            return render_template('blank.html',
                                   message='Пароль успешно изменен')

    return render_template('change_password.html',
                           form=form)


@app.route('/logs')
@login_required
def logs():
    if 'username' in session:
        username = session['username']
        if username == ADMIN_LOGIN:
            log = ActionLog.query.all()
            action_log(username, 'log to admin panel')
            return render_template('admin_logs.html',
                                   user=username,
                                   messages=log)
