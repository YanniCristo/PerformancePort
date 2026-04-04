from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from flask_login import UserMixin
from db.database import engine

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)

