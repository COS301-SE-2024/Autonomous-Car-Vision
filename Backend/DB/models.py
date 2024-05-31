from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Construct the database URL
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    uname = Column(String, unique=True, nullable=False)
    uemail = Column(String, unique=True, nullable=False)

class Auth(Base):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
    hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    user = relationship('User')

class Otp(Base):
    __tablename__ = 'otp'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
    otp = Column(String(6))
    creation_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    user = relationship('User')
