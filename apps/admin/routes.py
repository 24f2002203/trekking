from flask import Blueprint, render_template, request, redirect, url_for, flash
from .add_treks_form import AddTreksForm
from .update_treks_form import UpdateTreksForm
from core.models import Treks, User, Bookings, StaffAssignments, Role
from datetime import datetime, UTC, date
from database import db
from sqlalchemy.orm import aliased 
from sqlalchemy import or_, cast, String

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
    S = aliased(StaffAssignments)
    U = aliased(User)
    data = ( 
            db.session.query(T, S, U)
            .outerjoin(S, T.trek_id == S.trek_id)
            .outerjoin(U, S.staff_id == U.id)
            .order_by(T.start_date.asc())
    )

    data = data.order_by(T.start_date.asc()).all()
    pending_staff_members = User.query.join(User.role).filter(Role.name == "staff", User.status == 'pending').all()
    approved_staff_members = User.query.join(User.role).filter(Role.name == "staff", User.status == 'approved').all()
    blacklisted = User.query.filter(User.status=='blacklisted').all()
    users = User.query.join(User.role).filter(Role.name == "user", User.status == 'approved').all()
    booking_records = (
        db.session.query(Bookings, User, Treks)
        .join(User, Bookings.user_id == User.id)
        .join(Treks, Bookings.trek_id == Treks.trek_id)
        .order_by(Bookings.booking_date.desc())
        .all()
    )
    trek_history = (
        db.session.query(Bookings, User, Treks)
        .join(User, Bookings.user_id == User.id)
        .join(Treks, Bookings.trek_id == Treks.trek_id)
        .filter(Bookings.status == "Completed")
        .order_by(Bookings.completion_date.desc())
        .all()
    )

    return render_template('admin/admin_dashboard.html', 
                           data = data, 
                           pending_staff_members = pending_staff_members, 
                           approved_staff_members = approved_staff_members, 
                           blacklisted = blacklisted, 
                           booking_records = booking_records,
                           trek_history = trek_history,
                           users = users)

@blueprint.route('/view_all_treks')
def view_all_treks():
    T = aliased(Treks)
    S = aliased(StaffAssignments)
    U = aliased(User)
    data = ( 
            db.session.query(T, S, U)
            .outerjoin(S, T.trek_id == S.trek_id)
            .outerjoin(U, S.staff_id == U.id)
            .order_by(T.start_date.asc())
    )

    data = data.order_by(T.start_date.asc()).all()

    return render_template('admin/view_all_treks.html', data = data)

@blueprint.route('/view_all_staff')
def view_all_staff():

    data = ( 
            User.query.filter(
                User.role.has(name = "staff")
            )
    )

    data = data.order_by(User.id.asc()).all()

    return render_template('admin/view_all_staff.html', data = data)

@blueprint.route('/view_all_users')
def view_all_users():

    data = ( 
            User.query.filter(
                User.role.has(name = "user")
            )
    )

    data = data.order_by(User.id.asc()).all()

    return render_template('admin/view_all_users.html', data = data)

@blueprint.route('/view_trek_users/<int:trek_id>')
def view_trek_users(trek_id):

    T = aliased(Treks)
    B = aliased(Bookings)
    U = aliased(User)
    S = aliased(StaffAssignments)

    data = (
        db.session.query(T, B, U)
        .join(B, B.trek_id == T.trek_id)
        .join(U, B.user_id == U.id)
        .filter(T.trek_id == trek_id)
    )

    data = data.order_by(U.id.asc()).all()

    trek = Treks.query.filter_by(trek_id = trek_id).first()

    staff = (
        db.session.query(U)
        .join(S, S.staff_id == U.id)
        .filter(S.trek_id == trek_id)
        .first()
    )

    return render_template('admin/view_trek_users.html', data = data, staff=staff, trek = trek)

@blueprint.route('/add_treks', methods = ['GET', 'POST'])
def add_treks(): 

    form = AddTreksForm() 

    if request.method == 'GET': 
        form.user_name.data = "Admin"
        return render_template('admin/add_treks.html', form = form) 
    
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
                available_member_slots = form.member_slots.data,
                status = form.status.data.lower(),
                start_date = (form.start_date.data),
                end_date = (form.end_date.data),
                created_at = date.today(),
            ) 
            db.session.add(new_trek)
            trek = Treks.query.order_by(Treks.trek_id.desc()).first()

            if form.staff_first_name.data and form.staff_last_name.data and form.staff_email.data:
                staff_assigned = User.query.filter(
                    User.first_name == form.staff_first_name.data,
                    User.last_name == form.staff_last_name.data,
                    User.email == form.staff_email.data
                ).first()

                if staff_assigned.status == 'blacklisted': 
                    message = "The assigned staff is blacklisted and cannot be part of the program anymore"
                    flash(message)
                    return redirect(url_for('admin.add_treks'))

                staff_assignment = StaffAssignments(
                    staff_id = staff_assigned.id,
                    trek_id = trek.trek_id,
                    assigned_at = date.today()
                )
                db.session.add(staff_assignment)

            db.session.commit()

    return redirect(url_for('admin.dashboard') )

@blueprint.route('/update_trek/<int:trek_id>', methods = ['GET', 'POST'])
def update_trek(trek_id):

    trek = Treks.query.filter(Treks.trek_id == trek_id).first()
    staff_assignment = StaffAssignments.query.filter(StaffAssignments.trek_id == trek_id).first()
    staff = None
    if staff_assignment:
        staff = User.query.get(staff_assignment.staff_id)
    form = UpdateTreksForm(obj=trek)

    if request.method == 'GET': 
        
        return render_template('admin/update_treks.html', form = form, trek = trek, staff=staff)
    
    if request.method == "POST": 

        cols = ['trek_name', 'location', 'district', 'state', 'pincode', 'difficulty', 'duration', 'member_slots', 'status', 'start_date', 'end_date']

        for col in cols:
            value = getattr(form, col).data

            if value is not None and value != "":
                setattr(trek, col, value)
        
        if form.staff_first_name or form.staff_last_name or form.staff_email:
            staff = User.query.filter(
                User.first_name == form.staff_first_name.data,
                User.last_name == form.staff_last_name.data,
                User.email == form.staff_email.data
            ).first()

            if not staff:
                message = "Staff member not found."
                return render_template(
                    "admin/error.html",
                    message = message
                )

            if staff.status == "blacklisted":
                message = "Your account has been blacklisted by the admin, you cannot access the website"
                return render_template("admin/error.html", message = message)

            if staff_assignment:
                staff_assignment.staff_id = staff.id
            else:
                staff_assignment = StaffAssignments(
                    trek_id=trek.trek_id,
                    staff_id=staff.id
                )
                db.session.add(staff_assignment)

            db.session.commit()

        return redirect(url_for('admin.dashboard'))

@blueprint.route('/delete_trek/<int:trek_id>', methods = ['GET', 'POST'])
def delete_trek(trek_id):
    
    existing_trek = Treks.query.filter(Treks.trek_id == trek_id).first()
    existing_staff_assignment = StaffAssignments.query.filter(StaffAssignments.trek_id == trek_id).first()

    db.session.delete(existing_trek)
    db.session.delete(existing_staff_assignment)
    db.session.commit() 

    return redirect(url_for('admin.dashboard'))

@blueprint.route('/search_treks')
def search_treks():

    T = aliased(Treks)
    S = aliased(StaffAssignments)
    U = aliased(User)

    search = request.args.get("search", "")

    query = (
        db.session.query(T, S, U)
        .outerjoin(S, T.trek_id == S.trek_id)
        .outerjoin(U, S.staff_id == U.id)
    )

    if search:
        query = query.filter(
            or_(
                T.trek_name.ilike(f"%{search}%"),
                T.location.ilike(f"%{search}%"),
                cast(T.trek_id, String).ilike(f"%{search}%"),
                T.difficulty.ilike(f"%{search}%"),
                cast(T.duration, String).ilike(f"%{search}%"),
                cast(T.start_date, String).ilike(f"%{search}%"),
                cast(T.end_date, String).ilike(f"%{search}%"),

                U.first_name.ilike(f"%{search}%"),
                U.last_name.ilike(f"%{search}%"),
                cast(U.id, String).ilike(f"%{search}%"),
            )
        )

    data = query.order_by(T.start_date.asc()).all()

    return render_template(
        "admin/search_treks.html",
        data=data
    )
    
@blueprint.route('/search_staff', methods = ['GET'])
def search_staff(): 

    search = request.args.get("search", "")

    query = User.query.filter(
        User.role.has(name = "staff")
    )

    if search:
        query = query.filter(
            or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                cast(User.id, String).ilike(f"%{search}%"),
                User.status.ilike(f"%{search}%"),
            )
        )

    data = query.order_by(User.id.asc()).all()

    return render_template(
        "admin/search_staff.html",
        data=data
    )

@blueprint.route('/search_users', methods = ['GET'])
def search_users(): 
    search = request.args.get("search", "")

    query = User.query.filter(
        User.role.has(name = "user")
    )

    if search:
        query = query.filter(
            or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                cast(User.id, String).ilike(f"%{search}%"),
            )
        )

    data = query.order_by(User.id.asc()).all()

    return render_template(
        "admin/search_users.html",
        data=data
    )

    
@blueprint.route('/assign_trek/<int:staff_id>', methods = ['GET', 'POST'])
def assign_trek(staff_id): 
    staff = User.query.filter(User.id == staff_id).first()
    if staff.status == 'blacklisted': 
        return render_template('admin/blacklisted_user.html')
    
    if request.method == "GET": 
        assigned_treks = (
            db.session.query(Treks, StaffAssignments, User)
            .outerjoin(StaffAssignments, Treks.trek_id == StaffAssignments.trek_id)
            .outerjoin(User, StaffAssignments.staff_id == User.id)
            .filter(StaffAssignments.staff_id == staff_id)
            .all()
        )
        other_treks = (
            db.session.query(Treks)
            .outerjoin(
                StaffAssignments,
                Treks.trek_id == StaffAssignments.trek_id
            )
            .filter(StaffAssignments.trek_id == None)
            .all()
        )
        return render_template('admin/assign_staff_to_trek.html', assigned_treks = assigned_treks, other_treks = other_treks, staff=staff)
    
    if request.method == "POST": 
        trek_id = request.form.get('trek_id')
        assignment = StaffAssignments(
            staff_id = staff_id,
            trek_id = trek_id,
            assigned_at = date.today()
        )
        db.session.add(assignment)
        db.session.commit()

        assigned_treks = (
            db.session.query(Treks, StaffAssignments, User)
            .outerjoin(StaffAssignments, Treks.trek_id == StaffAssignments.trek_id)
            .outerjoin(User, StaffAssignments.staff_id == User.id)
            .filter(StaffAssignments.staff_id == staff_id)
            .all()
        )
        other_treks = (
            db.session.query(Treks)
            .outerjoin(
                StaffAssignments,
                Treks.trek_id == StaffAssignments.trek_id
            )
            .filter(StaffAssignments.trek_id == None)
            .all()
        )
        return render_template('admin/assign_staff_to_trek.html', assigned_treks = assigned_treks, other_treks = other_treks, staff=staff)
    
@blueprint.route('/unassign_trek/<int:staff_id>/<int:trek_id>')
def unassign_trek(staff_id, trek_id):

    assignment = StaffAssignments.query.filter_by(
        staff_id=staff_id,
        trek_id=trek_id
    ).first()

    if assignment is None:
        flash("Assignment not found.")
        return redirect(url_for('admin.assign_trek', staff_id=staff_id))

    db.session.delete(assignment)
    db.session.commit()

    flash("Trek unassigned successfully.")
    return redirect(url_for('admin.assign_trek', staff_id=staff_id))

    
@blueprint.route('/approve_staff/<int:staff_id>', methods = ['GET', 'POST'])
def approve_staff(staff_id):
    staff = User.query.filter(User.id == staff_id).first()
    staff.status = 'approved'
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@blueprint.route('/view_staff_treks/<int:staff_id>', methods = ['GET', 'POST'])
def view_staff_treks(staff_id):

    T = aliased(Treks)
    S = aliased(StaffAssignments)
    U = aliased(User)

    data = (
        db.session.query(T, S, U)
        .join(S, T.trek_id == S.trek_id)
        .join(U, S.staff_id == U.id)
        .filter(U.id == staff_id)
        .all()
    )

    staff_name = User.query.filter(User.id == staff_id).first()

    return render_template('admin/view_staff_treks.html', data = data, staff_name=staff_name)

@blueprint.route('/blacklist_user/<int:user_id>')
def blacklist_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    user.status = 'blacklisted'
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@blueprint.route('/allowlist_user/<int:user_id>')
def allowlist_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    user.status = 'approved'
    db.session.commit()
    return redirect(url_for('admin.dashboard'))