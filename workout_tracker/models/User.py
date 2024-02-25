from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    encrypted_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)

    def set_password(self, password):
        self.encrypted_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.encrypted_password, password)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)
