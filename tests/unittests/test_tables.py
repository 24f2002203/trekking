import os, sys 
from sqlalchemy import inspect 
import pytest 

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app import app 
from application.database import db

@pytest.fixture()
def inspector():
    with app.app_context():
        inspector = inspect(db.engine)
        yield inspector

def test_tables_exist(inspector):
    tables = inspector.get_table_names()
    print(tables)
    assert 'users' in tables 
    assert 'treks' in tables 
    assert 'staff_assignments' in tables 
    assert 'bookings' in tables 
    assert 'blacklist' in tables 

