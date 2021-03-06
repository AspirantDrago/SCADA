from .db_session import SqlAlchemyBase, orm
import sqlalchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    role_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("roles.id"), nullable=False, default=3)
    role = orm.relation('Roles', backref='users')
    temperature_id = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey("temperature.id"), nullable=False, default=1)
    temperature = orm.relation('Temperature', backref='users')
    pressure_id = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey("pressure.id"), nullable=False, default=1)
    pressure = orm.relation('Pressure', backref='users')
    consumption_id = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey("consumption.id"), nullable=False, default=1)
    consumption = orm.relation('Consumption', backref='users')
    reduced_consumption = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __str__(self):
        return self.login

    def __repr__(self):
        return f'<User {self.id} "{self.login}">'

    @property
    def created_date_format(self):
        return self.created_date.strftime("%d.%m.%Y")
