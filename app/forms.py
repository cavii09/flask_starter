from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired


class PropertyForm(FlaskForm):
    property_title = StringField('Title', validators=[InputRequired()])
    bathrooms   = IntegerField('Bathrooms', validators=[InputRequired()])
    bedrooms    = IntegerField('Rooms', validators=[InputRequired()])
    location    = StringField('Location', validators=[InputRequired()])
    price       =  IntegerField('Price', validators=[InputRequired()])
    property_type = SelectField('type', choices=[('house', 'House'), ('apt', 'Apartment')])
    description = TextAreaField('Description', validators=[InputRequired()])
    photo       = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!') ])