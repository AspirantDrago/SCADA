from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms_strip import StrippedPasswordField, StrippedStringField


class LoginForm(FlaskForm):
    login = StrippedStringField('Логин', validators=[
        DataRequired(message='Введите логин'),
    ])
    password = StrippedPasswordField('Пароль', validators=[
        DataRequired(message='Введите пароль')
    ])
    submit = SubmitField('Вход')
