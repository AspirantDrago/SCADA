from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import \
    DataRequired, Length as LengthValidator, Regexp as RegexpValidator
from .wtforms_strip import StrippedStringField


class EditLoginForm(FlaskForm):
    new_login = StrippedStringField('Новый логин', validators=[
        DataRequired(message='Введите новый логин'),
    ])
    submit = SubmitField('Сменить логин')
