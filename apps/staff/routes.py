from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app as app
from flask_login import current_user
from sqlalchemy.orm import aliased
from sqlalchemy import or_, cast, String
from sqlalchemy import func
from database import db
from core.models import Treks, StaffAssignments, User, Bookings
from .update_treks_form import UpdateTreksForm
from datetime import datetime


blueprint = Blueprint(
    'staff', 
    __name__, 
    url_prefix='/staff'
)
def is_assigned_staff(trek_id):

    assignment = StaffAssignments.query.filter_by(
        trek_id=trek_id,
        staff_id=current_user.id
    ).first()

    return assignment is not None

@blueprint.route('/test')
def test_staff(): 
    return {"message":"Staff route is working"} 

@blueprint.route('/dashboard')
def dashboard():

    T = aliased(Treks)
    S = aliased(StaffAssignments)
    U = aliased(User)

    staff = User.query.filter_by(id=current_user.id).first()

    data = (
    db.session.query(
        T,
        S,
        U,
        func.count(Bookings.booking_id).label("trekkers")
    )
    .join(S, T.trek_id == S.trek_id)
    .join(U, S.staff_id == U.id)
    .outerjoin(
        Bookings,
        (Bookings.trek_id == T.trek_id) &
        (Bookings.status == "Booked")
    )
    .filter(U.id == current_user.id)
    .group_by(T.trek_id, S.assignment_id, U.id)
    .all()
)
    return render_template('staff/staff_dashboard.html', data = data,  staff = staff)

@blueprint.route('/update_treks/<int:trek_id>', methods = ['GET', 'POST'])
def update_treks(trek_id):

    trek = Treks.query.filter(Treks.trek_id == trek_id).first()
    form = UpdateTreksForm(obj=trek)

    if request.method == "GET":

        return render_template('staff/update_treks.html', form = form, trek = trek, staff_id = current_user.id)
    
    elif request.method == "POST": 

        editable_cols = ['member_slots', 'status']

        for col in editable_cols:
            value = getattr(form, col).data

            if value is not None and value != "":
                setattr(trek, col, value)

        

        db.session.commit()
        return redirect(url_for('staff.dashboard', staff_id = current_user.id ))   

@blueprint.route("/view_trek_users/<int:trek_id>")
def view_trek_users(trek_id):

    if not is_assigned_staff(trek_id):
        return render_template('staff/error.html', message = "You can only update assigned treks", staff_id = current_user.id)

    trek = Treks.query.get_or_404(trek_id)

    users = (
        db.session.query(Bookings, User)
        .join(User, Bookings.user_id == User.id)
        .filter(
            Bookings.trek_id == trek_id,
            Bookings.status == "Booked"
        )
        .all()
    )

    return render_template(
        "staff/view_trek_users.html",
        trek=trek,
        users=users
    )

@blueprint.route("/start_trek/<int:trek_id>")
def start_trek(trek_id):

    if not is_assigned_staff(trek_id):
        return render_template('staff/error.html', message = "You can only update assigned treks", staff_id = current_user.id)

    trek = Treks.query.get_or_404(trek_id)

    trek.status = "Started"

    db.session.commit()

    flash("Trek started.")

    return redirect(url_for("staff.dashboard"))

@blueprint.route("/ongoing_trek/<int:trek_id>")
def ongoing_trek(trek_id):

    if not is_assigned_staff(trek_id):
        return render_template('staff/error.html', message = "You can only update assigned treks", staff_id = current_user.id)

    trek = Treks.query.get_or_404(trek_id)

    trek.status = "Ongoing"

    db.session.commit()

    flash("Trek is now ongoing.")

    return redirect(url_for("staff.dashboard"))

@blueprint.route("/complete_trek/<int:trek_id>")
def complete_trek(trek_id):

    if not is_assigned_staff(trek_id):
        return render_template('staff/error.html', message = "You can only update assigned treks", staff_id = current_user.id)

    trek = Treks.query.get_or_404(trek_id)

    trek.status = "Completed"

    bookings = Bookings.query.filter_by(
        trek_id=trek_id,
        status="Booked"
    ).all()

    for booking in bookings:

        booking.status = "Completed"
        booking.completion_date = datetime.utcnow()

    db.session.commit()

    flash("Trek completed.")

    return redirect(url_for("staff.dashboard"))

@blueprint.route("/remove_participant/<int:booking_id>")
def remove_participant(booking_id):

    booking = Bookings.query.get_or_404(booking_id)

    if not is_assigned_staff(booking.trek_id):
        return render_template('staff/error.html', message = "You can only update assigned treks", staff_id = current_user.id)

    booking.status = "Cancelled"

    trek = Treks.query.get(booking.trek_id)
    trek.available_member_slots += 1

    db.session.commit()

    flash("Participant removed.")

    return redirect(
        url_for(
            "staff.view_trek_users",
            trek_id=booking.trek_id
        )
    )

@blueprint.route('/search_treks')
def search_treks():

    T = aliased(Treks)
    S = aliased(StaffAssignments)
    U = aliased(User)

    search = request.args.get("search", "")

    query = (
        db.session.query(T, S, U)
        .join(S, T.trek_id == S.trek_id)
        .join(U, S.staff_id == U.id)
        .filter(U.id == current_user.id)
    )

    if search:
        query = query.filter(
            or_(
                cast(T.trek_id, String).ilike(f"%{search}%"),
                T.trek_name.ilike(f"%{search}%"),
                T.location.ilike(f"%{search}%"),
                T.difficulty.ilike(f"%{search}%"),
                T.status.ilike(f"%{search}%"),
                cast(T.duration, String).ilike(f"%{search}%"),
                cast(T.start_date, String).ilike(f"%{search}%"),
                cast(T.end_date, String).ilike(f"%{search}%"),
                U.first_name.ilike(f"%{search}%"),
                U.last_name.ilike(f"%{search}%"),
            )
        )

    data = query.order_by(T.start_date.asc()).all()

    return render_template(
        "staff/search_treks.html",
        data=data,
        staff_id=current_user.id
    )