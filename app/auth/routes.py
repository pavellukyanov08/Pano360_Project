from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user

from .forms import RegistrationForm, LoginForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from ..config import db

reg_user_page = Blueprint('register', __name__)
log_user_page = Blueprint('login', __name__)
logout_user_page = Blueprint('logout', __name__)


@reg_user_page.route("/admin/register", methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        try:
            username = reg_form.username.data
            password = reg_form.password.data

            user = User.query.filter_by(username=reg_form.username.data).first()

            if user is None:
                hashed_pw = generate_password_hash(password)
                user = User(
                    username=username,
                    hash_password=hashed_pw,
                )
                db.session.add(user)
                db.session.commit()
                flash('Вы успешно зарегистрированы!', 'success')
                return redirect(url_for('admin.index'))
            else:
                flash('Пользователь с таким логином уже существует!', 'danger')

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'danger')
    return render_template('auth/register.html', reg_form=reg_form)


@log_user_page.route("/admin/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        try:
            user = User.query.filter_by(username=login_form.username.data).first()
            if user:
                if user.verify_password(login_form.password.data):
                    login_user(user)
                    return redirect(url_for('admin.index'))
                else:
                    flash("Неверное или пользователя или пароль!", "danger")
            else:
                flash("Такого пользователя не существует!", 'danger')
        except Exception as e:
            flash(str(e), "danger")
    return render_template('auth/login.html', login_form=login_form)


@logout_user_page.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))

