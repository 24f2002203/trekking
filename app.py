import os, logging
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_login import LoginManager
from database import db
from config import LocalDevelopmentConfig, TestingConfig, LocalConfig
from apps import register_blueprints

logging.basicConfig(filename='debug.log', level = logging.DEBUG, format = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

security = Security()

login_manager = LoginManager()

user_datastore = None

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
        from core.models import User, Treks, StaffAssignments, Bookings, Role
        user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

        
        login_manager.login_view = 'authentication.login'
        login_manager.init_app(app)
        #security.init_app(app, app.user_datastore)
        '''Mail(app)'''
        security.init_app(app, user_datastore)
        register_blueprints(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
 
    return app 

app = create_app()




if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port=5000)