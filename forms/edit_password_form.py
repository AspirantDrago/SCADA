from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import \
    DataRequired, Length as LengthValidator, Regexp as RegexpValidator, EqualTo
from .wtforms_strip import StrippedPasswordField, StrippedStringField

from config import MIN_PASSWORD_LENGTH


class EditPasswordForm(FlaskForm):
    last_password = StrippedPasswordField('Старый пароль', validators=[
        DataRequired(message='Введите старый пароль'),
    ])
    password = StrippedPasswordField('Новый пароль', validators=[
        DataRequired(message='Введите новый пароль'),
        LengthValidator(min=MIN_PASSWORD_LENGTH,
                        message=f'Длина пароля должна быть более {MIN_PASSWORD_LENGTH} символов'),
        RegexpValidator(r'(?=.*[a-zA-Z])(?=.*[0-9])', flags=0,
                        message='Пароль должен содержать цифры и буквы латинского алфавита')
    ])
    password_2 = StrippedPasswordField('Повторите пароль', validators=[
        DataRequired(message='Введите пароль ещё раз'),
        EqualTo('password', 'Пароли не совпадают')
    ])
    submit = SubmitField('Сменить пароль')
