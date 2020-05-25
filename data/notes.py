from .db_session import SqlAlchemyBase, orm
import sqlalchemy
import datetime


class Note(SqlAlchemyBase):
    __tablename__ = 'notes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"), nullable=False)
    user = orm.relation('User', backref='notes')
    data = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
