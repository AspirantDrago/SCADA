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

    def __repr__(self):
        return f'<Note {self.id} {self.user} "{self.data[:10]}" {self.created_date_format}>'

    @property
    def created_date_format(self):
        return self.created_date.strftime("%d.%m.%Y %H:%M")

    def data_format(self, rows=None, max_length=None):
        data = self.data.splitlines()
        if rows:
            data = data[:rows]
        return '\r\n'.join(data)
