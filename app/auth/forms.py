from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(),
        Length(5, 50, message="Имя пользователя должно содержать от 4 до 50 символов")
    ])

    # email = StringField('Емайл', validators=[
    #     Email(),
    #     Length(10, 50, message="Введите действительный емайл")
    # ])

    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=5, message='Пароль должен содержать минимум 5 символов')
    ])

    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать'),
    ])

    # @staticmethod
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         flash('Имя пользователя уже занят. Выберите другое', 'danger')
    #
    # @staticmethod
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         flash('Емаил пользователя уже занят. Выберите другой', 'danger')


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')