from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import date, timedelta 

class UpdateTreksForm(FlaskForm):
    user_name = StringField('User Name' )
    trek_name = StringField('Trek Name' )
    location = StringField('Location' )
    district = StringField('district')
    state = StringField('state')
    pincode = StringField('pincode')
    difficulty = StringField('Difficulty' )
    duration = StringField('Duration' )
    member_slots = IntegerField('Member Slots' )
    status = StringField('Status' )
    start_date = DateField('Start Date', default = date.today )
    end_date = DateField('End Date', default = date.today() + timedelta(days=3) )
    booking_date = DateField('Booking Date', default = date.today )
    booking_status = StringField('Booking Status' )
    submit = SubmitField('Update Trek')