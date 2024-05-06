from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileSize
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired

from main import projectsphotos, projectarchives


class PostProjForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    proj_type = SelectField('Тип', choices=['PyQt', 'pygame', 'WEB', 'Другое'], default=1)
    platform = StringField('Платформа')
    short_description = TextAreaField("Краткое описание")
    detailed_description = TextAreaField("Подробное описание")
    archive = FileField('Архив, только zip', validators=[FileAllowed(projectarchives, 'ZIP only!'),
                                             FileRequired('File was empty!'),
                                             FileSize(50000000, message='No more than 50 MB!')])
    image = FileField('Обложка, только png', validators=[FileAllowed(projectsphotos, 'PNG only!'),
                                             FileRequired('File was empty!'),
                                             FileSize(50000000, message='No more than 50 MB!')])
    submit = SubmitField('Отправить проект')
