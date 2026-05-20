import os, sys, pytest 
from sqlalchemy import inspect 

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app import app 
from application.database import db 

@pytest.fixture()
def inspector():
    with app.app_context():
        inspector = inspect(db.engine)
        yield inspector

def get_columns(inspector, table_names): 
    columns_list = inspector.get_columns(table_names)
    columns = [column['name'] for column in columns_list] 
    return columns 


def test_users_columns(inspector):
    columns = get_columns(inspector, 'users')

    assert 'user_id' in columns
    assert 'name' in columns
    assert 'email' in columns
    assert 'password' in columns
    assert 'role' in columns
    assert 'contact' in columns
    assert 'status' in columns
    assert 'created_at' in columns

def test_treks_columns(inspector):
    columns = get_columns(inspector, 'treks')

    assert 'trek_id' in columns
    assert 'trek_name' in columns
    assert 'location' in columns
    assert 'difficulty' in columns
    assert 'duration' in columns
    assert 'available_slots' in columns
    assert 'status' in columns
    assert 'start_date' in columns
    assert 'end_date' in columns
    assert 'created_at' in columns
    assert 'created_by' in columns

def test_staff_assignments_columns(inspector):
    columns = get_columns(inspector, 'staff_assignments')

    assert 'assignment_id' in columns
    assert 'staff_id' in columns
    assert 'trek_id' in columns
    assert 'assigned_at' in columns

def test_bookings_columns(inspector):
    columns = get_columns(inspector, 'bookings')

    assert 'booking_id' in columns
    assert 'user_id' in columns
    assert 'trek_id' in columns
    assert 'booking_date' in columns
    assert 'status' in columns

def test_blacklist_columns(inspector):
    columns = get_columns(inspector, 'blacklist')

    assert 'blacklist_id' in columns
    assert 'user_id' in columns
    assert 'reason' in columns
    assert 'blacklisted_at' in columns