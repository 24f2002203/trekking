from database import db 
from app import create_app
from core.models import Role, User
from flask_security.utils import hash_password 
from flask_security import SQLAlchemySessionUserDatastore
from datetime import datetime, UTC
import uuid 

def create_default_roles(user_datastore): 

    roles = ['admin', 'staff', 'user']

    for role in roles: 
    
        existing_role =  Role.query.filter(Role.name == role).first()

        if not existing_role: 

            new_role = Role(name=role)
            db.session.add(new_role)

    db.session.commit()

def create_admin_account(user_datastore): 

    existing_admin = User.query.filter(User.role.has(name = 'admin')).first() 

    if not existing_admin: 

        admin_user = User(
            first_name = 'Admin_user', 
            email = 'admin@gmail.com',
            password = ('admin1234'),
            contact = '1234567890', 
            status = 'approved',
            created_at = datetime.now(UTC),
            fs_uniquifier = str(uuid.uuid4())
        )

        admin_user.role = Role.query.filter_by(name="admin").first()
        
        db.session.add(admin_user)
        db.session.commit()

app = create_app()

print("Creating default roles ... ")

with app.app_context():
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

    create_default_roles(user_datastore)
    create_admin_account(user_datastore)

print("Created Roles")