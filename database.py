from sqlalchemy.orm import declarative_base
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

engine = None

Base = declarative_base()