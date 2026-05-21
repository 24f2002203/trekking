from app import app 
from application.database import db
from flask import render_template, redirect, url_for

@app.route('/')
def home():
    return render_template('home.html')