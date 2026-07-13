from flask import Blueprint, render_template, redirect, url_for, flash

blueprint = Blueprint(
    'staff', 
    __name__, 
    url_prefix='/staff'
)

@blueprint.route('/test')
def test_staff(): 
    return {"message":"Staff route is working"} 

@blueprint.route('/dashboard')
def dashboard():
    return render_template('staff_dashboard.html')