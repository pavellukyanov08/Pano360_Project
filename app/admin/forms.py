from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired, Length


class SectionForm(FlaskForm):
    title = StringField('Название раздела', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired(), Length(min=1, max=100)])
    sort_in_list = IntegerField('Сортировка в списке', validators=[DataRequired()])
    cover_proj = FileField('Обложка раздела', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Только изображения!')
    ])  # Поле для загрузки изображения
