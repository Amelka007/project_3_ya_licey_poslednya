import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class ChangeLog(SqlAlchemyBase):
    __tablename__ = 'Change_log'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.id"))
    record_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    table_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)

    user = orm.relationship('User')
