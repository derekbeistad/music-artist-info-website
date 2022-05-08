from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ArtistSearch(FlaskForm):
    artist_name = StringField('Artist Name: ', validators=[DataRequired()])
    submit = SubmitField('Search')


class SongSearch(FlaskForm):
    song_name = StringField('Song Name')
    submit = SubmitField('Search')
