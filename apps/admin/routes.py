from flask import Blueprint, render_template, request, redirect, url_for, flash
from .add_treks_form import AddTreksForm
from .update_treks_form import UpdateTreksForm
from core.models import Treks, User, Bookings
from datetime import datetime, UTC, date
from database import db
from sqlalchemy.orm import aliased 

blueprint = Blueprint(
    'admin', 
    __name__, 
    url_prefix='/admin'
)

@blueprint.route('/test')
def test_admin(): 
    return {"message":"Admin route is working"} 

@blueprint.route('/dashboard')
def dashboard():
    T = aliased(Treks)
    B = aliased(Bookings)
    data = db.session.query(T, B).join(T, B.trek_id==T.trek_id).all()
    return render_template('admin_dashboard.html', data = data)

@blueprint.route('/add_treks', methods = ['GET', 'POST'])
def add_treks(): 

    form = AddTreksForm() 

    if request.method == 'GET': 
        form.user_name.data = "Admin"
        return render_template('add_treks.html', form = form) 
    
    elif request.method == 'POST': 
        

        if form.trek_name.data and form.location.data : 

            new_trek = Treks (
                trek_name = form.trek_name.data, 
                location = form.location.data,
                district = form.district.data,
                state = form.state.data,
                pincode = form.pincode.data,
                difficulty = form.difficulty.data.lower(),
                duration = form.duration.data,
                member_slots = form.member_slots.data,
                status = form.status.data.lower(),
                start_date = (form.start_date.data),
                end_date = (form.end_date.data),
                created_at = date.today(),
            ) 
            db.session.add(new_trek)
            trek = Treks.query.order_by(Treks.trek_id.desc()).first()
            if trek: 
                booking_status = "confirmed"
            else: 
                booking_status = "pending"

            new_booking = Bookings(
                trek_id = trek.trek_id, 
                booking_date = date.today(), 
                status = str(booking_status).lower() 
            )
            db.session.add(new_booking)

            db.session.commit()

    return redirect(url_for('admin.dashboard') )

@blueprint.route('/update_trek/<int:trek_id>', methods = ['GET', 'POST'])
def update_trek(trek_id):

    
     
    trek = Treks.query.filter(Treks.trek_id == trek_id).first()
    booking = Bookings.query.filter(Bookings.trek_id == trek_id).first()

    form = UpdateTreksForm(obj=trek)
    form.booking_date.data = booking.booking_date
    form.booking_status.data = booking.status

    if request.method == 'GET': 
        
        return render_template('update_treks.html', form = form, trek = trek, booking = booking)
    
    if request.method == "POST": 

        cols = ['trek_name', 'location', 'district', 'state', 'pincode', 'difficulty', 'duration', 'member_slots', 'status', 'start_date', 'end_date']

        for col in cols:
            value = getattr(form, col).data

            if value is not None and value != "":
                setattr(trek, col, value)

        if form.booking_date.data: 

            booking.booking_date = form.booking_date.data 

        if form.booking_status.data: 

            booking.status = form.booking_status.data 

        db.session.commit()

        return redirect(url_for('admin.dashboard'))


@blueprint.route('/delete_trek/<int:trek_id>', methods = ['GET', 'POST'])
def delete_trek(trek_id):
    
    existing_trek = Treks.query.filter(Treks.trek_id == trek_id).first()
    existing_booking = Bookings.query.filter(Bookings.trek_id ==trek_id).first()

    db.session.delete(existing_trek)
    db.session.delete(existing_booking)
    db.session.commit() 

    return redirect(url_for('admin.dashboard'))