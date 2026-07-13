from flask import Blueprint, render_template, redirect, url_for, flash

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
    return render_template('user_dashboard.html')