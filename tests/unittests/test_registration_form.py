import os, sys, pytest 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app
from core.models import User 

@pytest.fixture 
def client(): 

    with app.app_context(): 

        client = app.test_client()

        yield client

def test_register_user(client): 

    response = client.get('/authentication/user/register', follow_redirects = True)

    assert b"Register" in response.data
    assert response.status_code == 200
    assert b"first_name" in response.data
    assert b"last_name" in response.data
    assert b"email" in response.data
    assert b"password" in response.data
    assert b"password_confirm" in response.data
    assert b"submit" in response.data