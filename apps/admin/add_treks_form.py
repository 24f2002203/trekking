from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import date, timedelta 

class AddTreksForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    trek_name = StringField('Trek Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    district = StringField('district')
    state = StringField('state')
    pincode = StringField('pincode')
    difficulty = StringField('Difficulty', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()])
    member_slots = IntegerField('Member Slots', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    start_date = DateField('Start Date', default = date.today, validators=[DataRequired()])
    end_date = DateField('End Date', default = date.today() + timedelta(days=3), validators=[DataRequired()])
    booking_date = DateField('Booking Date', default = date.today, validators=[DataRequired()])
    booking_status = StringField('Booking Status', validators=[DataRequired()])
    submit = SubmitField('Add Trek')