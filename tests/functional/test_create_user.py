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

def test_register_user(client): 

    user = User.query.filter(User.id == 2).first()

    if not user: 

        response = client.post('/register', data={
            'first_name': 'testuser',
            'last_name': 'last_name',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        })

        assert response.status_code == 201

        user = User.query.filter(User.email == 'test@example.com').first()

        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
