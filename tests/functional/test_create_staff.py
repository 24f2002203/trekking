import os, sys, pytest 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app
from core.models import User 
from database import db 
from datetime import datetime, UTC
import uuid

@pytest.fixture 
def client(): 

    with app.app_context(): 

        client = app.test_client()

        yield client

def test_register_staff(client): 

    response = client.post('/authentication/staff/register', follow_redirects = True)

    role = 'staff'

    user = User.query.order_by(User.id.desc() ).first()

    if not user: 
        
        user = User(
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoee@example.com',
            password = '123456',
            contact = '9123456789',
            created_at = datetime.now(UTC),
            fs_uniquifier = str(uuid.uuid4())
            )
            
        db.session.add(user)

        app.user_datastore.add_role_to_user(user, role)
        
        db.session.commit()

    id = int(user.id) +1
    first_name = f"test_{user.first_name}_{id}"
    last_name = f"test_{user.last_name}_{id}"
    email = f"test_{user.email}_{id}"
    password = f"test_{user.password}_{id}"
    confirm_password = f"test_{user.password}_{id}"

    response = client.post('/authentication/staff/register', data = dict(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password = password,
        confirm_password = confirm_password
    ), follow_redirects = True)

    check_user = User.query.filter(
        User.first_name == first_name,
        User.last_name == last_name,
        User.email == email
    ).first()
    
    role = User.role_name(check_user)
    assert check_user 
    assert response.status_code == 200
    assert role == 'staff'
