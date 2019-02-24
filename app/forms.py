from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SongForm(FlaskForm):
    song = StringField('Song', validators=[DataRequired()])
    artist = StringField('Artist (Optional)')
    submit = SubmitField('Enter')
