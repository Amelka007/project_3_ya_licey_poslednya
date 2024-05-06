import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

from models.users_projects import UserProject


class Project(SqlAlchemyBase):
    __tablename__ = 'Projects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    approved_or_not = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    project_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    project_type = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    archive = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    project_platform = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    project_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    short_description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_project = orm.relationship("UserProject", back_populates='project')
