from flask_security import UserMixin, RoleMixin
import  os, sys, uuid
from database import db
from datetime import datetime, UTC


roles_users = db.Table(
"roles_users",
db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    name = db.Column(db.String(100), nullable=False)
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)#why 100?
    password = db.Column(db.String(225), nullable=False)
    contact = db.Column(db.String(15))
    created_at = db.Column(db.DateTime(), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda:str(uuid.uuid4()))
    active = db.Column(db.Boolean(), default=True) 

    roles = db.relationship(
        "Role",
        secondary=roles_users,
        backref=db.backref("users", lazy="dynamic")
    )

    @classmethod
    def find_by_id(cls, _id: int) -> "User": 
        return cls.query.filter_by(id = _id).first()
    
    @classmethod
    def find_by_email(cls, _email: str) -> "User": 
        return cls.query.filter_by(email = _email).first()
    
    @classmethod
    def role_name(cls, user):
        return user.roles[0].name if user.roles else None


class Treks(db.Model):
    __tablename__ = 'treks'
    trek_id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    trek_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.Enum('easy', 'moderate', 'hard', name='dificulty_levels'), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    member_slots= db.Column(db.Integer(), nullable=False, default=0)
    status = db.Column(db.Enum('Complete', 'Ongoing','pending','open', 'closed', name='trek_status'), nullable=False, default='pending')
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    

class StaffAssignments(db.Model):
    __tablename__ = 'staff_assignments'
    assignment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False, unique=True)
    trek_id = db.Column(db.Integer(), db.ForeignKey('treks.trek_id'), nullable=False, unique=True)
    assigned_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(UTC))

class Bookings(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    trek_id = db.Column(db.Integer(), db.ForeignKey('treks.trek_id'), nullable=False)
    booking_date = db.Column(db.DateTime(), nullable=False, default=datetime.now(UTC))
    status = db.Column(db.Enum('confirmed', 'cancelled', 'pending', name='booking_status'), nullable=False, default='confirmed')

class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    blacklist_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False, unique=True)
    reason = db.Column(db.String(255), nullable=False)
    blacklisted_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(UTC))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)