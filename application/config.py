import os 

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