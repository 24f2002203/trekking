from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, DateField, SubmitField, EmailField
from wtforms.validators import Email
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
    staff_first_name = StringField("Staff First Name", validators=[DataRequired()])
    staff_last_name = StringField("Staff First Name", validators=[DataRequired()])
    staff_email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Trek')