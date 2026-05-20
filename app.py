import os, logging
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from application.database import db
from application.config import LocalDevelopmentConfig, TestingConfig, LocalConfig


logging.basicConfig(filename='debug.log', level = logging.DEBUG, format = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

def create_app():
    app = Flask(__name__, template_folder='templates')

    CORS(app)

    env = os.getenv('ENV', 'development')

    if env == 'production':
        app.logger.info("No production environment setup!")
        raise Exception("No prodcution environment is setup!")
    
    elif env == 'final_development':
        app.logger.info("Using local development testing configuration")
        app.config.from_object(LocalConfig)

    elif env == 'testing':
        app.logger.info("Using testing configuration")
        app.config.from_object(TestingConfig)

    else:
        app.logger.info("Using local development configuration")
        app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    Migrate(app, db) 
    with app.app_context():
        from application.models import Users, Treks, StaffAssignments, Bookings, blacklist
    return app 

app = create_app()

from application.controllers import *

if __name__ == '__main__':
    app.run(debug=True)