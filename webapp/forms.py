from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

class SelectImgForm(FlaskForm):
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-dark"})