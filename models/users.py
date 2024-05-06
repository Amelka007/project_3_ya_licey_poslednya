import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash

from .db_session import SqlAlchemyBase

from .users_settings import UserSettings
from .users_projects import UserProject
from .change_log import ChangeLog


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    reg_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now)
    role = sqlalchemy.Column(sqlalchemy.Integer, default=1)  # 1 - reged user
    user_role = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # надо не забыть дефолт добавить
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    github_ref = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    telegram_ref = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    platform = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    remember = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_settings = orm.relationship('UserSettings', back_populates='user')
    user_projects = orm.relationship('UserProject', back_populates='user')
    activity = orm.relationship('ChangeLog', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  #
        return check_password_hash(self.password_hash, password)
