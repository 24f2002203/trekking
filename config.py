import os, random, string, secrets
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join('./db_directory', 'trekking.sqlite3')
db_path = os.path.abspath(db_path)

dev_db_path = os.path.join('./db_directory', 'trekking_development.sqlite3')
dev_db_path = os.path.abspath(dev_db_path)

test_db_path = os.path.join('./db_directory', 'trekking_test.sqlite3')
test_db_path = os.path.abspath(test_db_path)

class BaseConfig:
    DEBUG=False 
    SQLITE_DB_DIR = None 
    SQLALCHEMY_DATABASE_URI = None 
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY: 
        SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for i in range(32))

    '''    USER_ROLES ={
        'USER':{
            'name':'USER', 
            'permissions': {'user-read', 'user-write'}
        }, 
        'STAFF':{
            'name':'STAFF', 
            'permissions': {'staff-read', 'staff-write'}
        }, 
        'ADMIN':{
            'name':'ADMIN', 
            'permissions': {'admin-read', 'admin-write'}
        }, 

    }

    EMAIL_SUBJECT_REGISTER = "Welcome to Trekking App! Please confirm your email"

    
    SECURITY_EMAIL_VALIDATOR_ARGS = { "check_deliverability": False}
    SECURITY_REGISTERABLE = os.environ.get('SECURITY_REGISTERABLE', True)
    SECURITY_CONFIRMABLE =  os.environ.get('SECURITY_CONFIRMABLE', True)
    SECURITY_RECOVERABLE= os.environ.get('SECURITY_RECOVERABLE', True)
    SECURITY_CHANGEABLE= os.environ.get('SECURITY_CHANGEABLE', True)
    SECURITY_SEND_REGISTER_EMAIL = os.environ.get('SECURITY_SEND_REGISTER_EMAIL', True)
    SECURITY_DEFAULT_REMEMBER_ME = os.environ.get('SECURITY_DEFAULT_REMEMBER_ME', True)
    SECURITY_POST_REGISTER_VIEW = '/authentication/login'
    SECURITY_POST_LOGOUT_VIEW = '/authentication/login'
    SECURITY_CHANGE_URL = '/authentication/change'#CHECK THIS AGAIN '''
    
    SESSION_COOKIE_SECURE = True 
    SECURITY_PASSWORD_HASH = os.environ.get('SECURITY_PASSWORD_HASH', 'bcrypt')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', secrets.token_hex(16))

    MAIL_BACKEND = os.environ.get('MAIL_BACKEND', 'console')

    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    SESSION_LIFETIME = timedelta(days=14)
    REMEBER_SESSION_LIFETIME = timedelta(days = 365)
    REMEBER_COOKIE_DURATION = REMEBER_SESSION_LIFETIME

class LocalDevelopmentConfig(BaseConfig):
    DEBUG=True 
    SQLITE_DB_DIR = dev_db_path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_DB_DIR

class LocalConfig(BaseConfig):
    DEBUG=True 
    SQLITE_DB_DIR = db_path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_DB_DIR

class TestingConfig(BaseConfig):
    DEBUG=True 
    SQLITE_DB_DIR = test_db_path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_DB_DIR