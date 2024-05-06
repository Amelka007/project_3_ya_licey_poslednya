import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class UserProject(SqlAlchemyBase):
    __tablename__ = 'Users_projects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.id"))
    project_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Projects.id"))

    user = orm.relationship('User')
    project = orm.relationship('Project')
