from datetime import timedelta 
from flask import Blueprint, render_template, request, session, current_app as app, redirect, url_for, flash
from flask_security.forms import LoginForm
from flask_security.utils import send_mail, logout_user,  hash_password, verify_password
from flask_security.signals import user_registered
from flask_login import login_user
from database import db 
from .registration_form import RegisterForm
import uuid
from datetime import datetime, UTC
from core.models import User, Role

blueprint = Blueprint(
    'authentication', 
    __name__, 
    url_prefix='/authentication'
)


@blueprint.route('/test')
def test_authentication(): 
    return {"message":"Authentication route is working"} 

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST': 

        if form.email.data and form.password.data: 
            
            email = form.email.data
            password = form.password.data 

            user = User.query.filter(User.email == email).first()

            if not user: 
                message = "User with this email does not exist. Please register first."
                return render_template('auth/error.html', message = message)

            role = User.role_name(user)
            
            if verify_password(password, user.password):

                login_user(user)

                if role == 'admin': 
                    return redirect(url_for('admin.dashboard'))
                elif role == 'staff' and user.status == 'approved':
                    return redirect(url_for('staff.dashboard', staff_id = user.id))
                elif role == 'staff' and user.status == 'pending':
                    message = "Your account is not yet approved by the admin."
                    return render_template('auth/error.html', message = message)
                elif role == 'user':
                    return redirect(url_for('user.dashboard'))
                else:
                    message = "Invalid role. Please contact the administrator."
                    return render_template('auth/error.html', message = message)
            else:
                message = "Incorrect email or password."
                return render_template('auth/error.html', message = message)
            
        else:
            message = "Please enter both email and password."
            return render_template('auth/error.html', message = message)
            
    else:
        return render_template('auth/login_form.html', form = form)

@blueprint.route('/<role>/register', methods = ['GET', 'POST'])
def register(role): 

    if role not in ['staff', 'user']: 
        message = "Invalid role"
        return render_template('auth/error.html', message = message)

    form = RegisterForm()

    if form.validate_on_submit():

        #if user is not already registered
        user = User.query.filter_by(email=form.email.data).first()
        if not user: 

            if form.password.data == form.password_confirm.data: 

                if len(form.password.data)>=8: 

                    if role == 'user': status = 'approved' 
                    else: status = 'pending'

                    role_id = Role.query.filter_by(name=role).first().id
                    user = User(
                        first_name = str(form.first_name.data).title(), 
                        last_name = str(form.last_name.data).title(),
                        email= form.email.data, 
                        password = hash_password(form.password.data),
                        contact = form.contact.data,
                        status = status.lower(), 
                        created_at = datetime.now(UTC),
                        role_id = role_id,
                        fs_uniquifier = str(uuid.uuid4())
                    )
                    db.session.add(user)

                    user.role = Role.query.filter_by(name=role).first()
                    
                    db.session.commit()
                    
                    return redirect(url_for('authentication.login'))
                
                else: 
                    message = "Password must be at least 8 characters long" 
                    return render_template('auth/error.html', message = message)
                
            else: 
                message = "Passwords do not match" 
                flash(message)
                return render_template('auth/error.html', message = message)
            
        else: 
            message = "User with this email already exists" 
            return render_template('auth/error.html', message = message)
        
    return render_template('auth/registration_form.html', form = form)