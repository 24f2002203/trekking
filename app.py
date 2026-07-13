import os, logging
from flask import Flask, session, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_security import SQLAlchemySessionUserDatastore
from flask_security.models import fsqla_v3 as fsqla
from flask_login import LoginManager
from flask_mailman import Mail
from database import db
from config import LocalDevelopmentConfig, TestingConfig, LocalConfig
from apps import register_blueprints
from extensions import  security 


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
    bcrypt = Bcrypt(app)
    Migrate(app, db) 
    


    with app.app_context():
        from core.models import User, Treks, StaffAssignments, Bookings, Blacklist, Role

        app.user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

        '''login = LoginManager(app)
        login.init_app(app)
        login.login_view = 'authentication.login'
        security.init_app(app, app.user_datastore)
        Mail(app)'''

        security.init_app(app, app.user_datastore)

        register_blueprints(app)
        
    return app 

app = create_app()

if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port=5000)