from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from core.models import Treks, User, Bookings
from database import db

blueprint = Blueprint(
    'user', 
    __name__, 
    url_prefix='/user'
)

@blueprint.route('/test')
def test_user(): 
    return {"message":"User route is working"} 

@blueprint.route('/dashboard')
def dashboard():

    user = current_user

    data = (
        Treks.query
        .filter(Treks.status == "open")
        .order_by(Treks.start_date.asc())
        .all()
    )

    booking_data = (
        db.session.query(Treks, Bookings)
        .join(Bookings, Treks.trek_id == Bookings.trek_id)
        .filter(Bookings.user_id == current_user.id)
        .order_by(Treks.start_date.asc())
        .all()
    )

    history = (
        db.session.query(Bookings, Treks)
        .join(Treks, Bookings.trek_id == Treks.trek_id)
        .filter(Bookings.user_id == current_user.id)
        .order_by(Bookings.booking_date.desc())
        .all()
    )

    return render_template(
        "user/user_dashboard.html",
        user=user,
        data=data,
        booking_data=booking_data, history = history
    )

@blueprint.route('/view_trek_details/<int:trek_id>')
def view_trek_details(trek_id):

    trek = Treks.query.filter_by(trek_id = trek_id).first()

    return render_template('user/view_trek_details.html', trek = trek, user_id=current_user.id)

@blueprint.route("/book_trek/<int:trek_id>")
def book_trek(trek_id):

    if current_user.status == "blacklisted":
        return render_template(
            "user/error.html",
            message="Your account has been blacklisted. You cannot book treks."
        )

    trek = Treks.query.get_or_404(trek_id)

    if trek.available_member_slots <= 0:
        return render_template(
            "user/error.html",
            message="No member slots are available for this trek."
        )

    existing = Bookings.query.filter(
        Bookings.user_id == current_user.id,
        Bookings.trek_id == trek_id,
        Bookings.status == "confirmed"
    ).first()

    if existing:
        return render_template(
            "user/error.html",
            message="You have already booked this trek.", staff_id = current_user.id
        )

    booking = Bookings(
        user_id=current_user.id,
        trek_id=trek_id,
        status="confirmed"
    )

    db.session.add(booking)

    trek.available_member_slots -= 1

    db.session.commit()

    return redirect(url_for("user.dashboard"))

@blueprint.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id): 

    user_id = current_user.id

    booking = Bookings.query.filter_by(booking_id = booking_id, user_id = user_id).first()
    db.session.delete(booking)
    db.session.commit() 

    return redirect(url_for('user.dashboard'))