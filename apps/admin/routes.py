from flask import Blueprint, render_template, request, redirect, url_for, flash

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
    return render_template('admin_dashboard.html')