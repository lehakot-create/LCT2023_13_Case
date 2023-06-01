from flask import render_template, redirect, session, url_for, request
from flask_login import login_user

# from app import app
from __init__ import app
from forms import LoginForm, ChangePassword
from models import ActionLog
from utils import hash_password
from config import ADMIN_LOGIN, ADMIN_PASSWORD
from database import db_session
from db_query import action_log, get_user, create_new_user, \
    change_user_password
from decorator import authorization_required, admin_only


@app.route('/')
@app.route('/index')
@authorization_required
def index():
    username = session['username']
    action_log(session.get('username', None), 'success log')
    return render_template('index.html',
                           user=username)


@app.route('/admin')
@admin_only
def admin():
    username = session['username']
    action_log(username, 'log to admin panel')
    return render_template('admin.html',
                           user=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user(username=form.name.data)
            username = form.name.data
            session['username'] = username
            key = hash_password(form.password.data)

            if username == ADMIN_LOGIN and key == ADMIN_PASSWORD:
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
@authorization_required
def logout():
    action_log(session['username'], 'log out')
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/create_user', methods=['GET', 'POST'])
@admin_only
def create_user():
    action_log(session.get('username', None), 'try create user')
    form = LoginForm()
    username = session['username']
    if request.method == 'POST':
        if form.validate_on_submit():
            user = form.name.data
            key = hash_password(form.password.data)
            try:
                create_new_user(name=user, password=key)
            except Exception as e:
                db_session.rollback()
                print(e)
                action_log(session.get('username', None), 'error create user')
                return render_template(
                    'blank_admin.html',
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
@authorization_required
def change_password():
    action_log(session.get('username', None), 'try change password')
    form = ChangePassword()
    user = get_user(username=session['username'])
    if request.method == 'POST':
        if form.validate_on_submit():

            old_password = form.old_password.data
            if hash_password(old_password) != user.password:
                action_log(session.get('username', None),
                           'error change password')
                return render_template('blank.html',
                                       message='Не корректный старый пароль')

            new_password = form.new_password.data
            repeat_new_password = form.repeat_new_password.data
            if new_password != repeat_new_password or new_password is None:
                action_log(session.get('username', None),
                           'error change password')
                return render_template('blank.html',
                                       message='Новые пароли не совпадают')
            try:
                change_user_password(user, hash_password(new_password))
            except Exception as e:
                db_session.rollback()
                print('Пароль уже используется', e)
                action_log(session.get('username', None),
                           'error change password')
                return render_template(
                    'blank.html',
                    message='Пароль уже используется. Выберите другой.')
            action_log(session.get('username', None),
                       'success change password')
            return render_template('blank.html',
                                   message='Пароль успешно изменен')

    return render_template('change_password.html',
                           form=form)


@app.route('/logs')
@admin_only
def logs():
    username = session['username']
    log = ActionLog.query.all()
    action_log(username, 'log to admin panel')
    return render_template('admin_logs.html',
                           user=username,
                           messages=log)
