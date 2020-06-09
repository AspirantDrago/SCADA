from .db_session import SqlAlchemyBase
import sqlalchemy


class Temperature(SqlAlchemyBase):
    __tablename__ = 'temperature'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    coefficient = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=1.0)
    shift = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0.0)

    def convert(self, value):
        return value * self.coefficient + self.shift

    def deconvert(self, value):
        return (value - self.shift) / self.coefficient

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Temperature {self.id} "{self.title}">'
