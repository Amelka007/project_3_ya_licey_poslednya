import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class UserSettings(SqlAlchemyBase):
    __tablename__ = 'Users_settings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.id"))
    is_email_visible = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_telegram_visible = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user = orm.relationship("User")
