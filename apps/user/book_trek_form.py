from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, DateField, SubmitField, EmailField
from wtforms.validators import Email
from wtforms.validators import DataRequired
from datetime import date, timedelta 

class BookTrekForm(FlaskForm): 
    ...