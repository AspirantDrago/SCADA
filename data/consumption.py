from .db_session import SqlAlchemyBase
import sqlalchemy


class Consumption(SqlAlchemyBase):
    __tablename__ = 'consumption'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    coefficient = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=1.0)
    shift = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0.0)

    def convert(self, value):
        return value * self.coefficient + self.shift

    def deconvert(self, value):
        return (value - self.shift) / self.coefficient