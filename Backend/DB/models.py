from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv
from pathlib import Path

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
    cid = Column(Integer, ForeignKey('corporations.cid', ondelete='CASCADE'), nullable=False)
    is_admin = Column(Boolean, default=False)
    last_signin = Column(DateTime, default=datetime.utcnow)

class Corporation(Base):
    __tablename__ = 'corporations'
    cid = Column(Integer, primary_key=True)
    cname = Column(String, unique=True, nullable=False)  
    
class TokenCorporation(Base):
    __tablename__ = 'token_corporation'
    tid = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
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
    
class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
    token = Column(String(40), unique=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    user = relationship('User')    

class Media (Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
    mid = Column(String, unique=True, nullable=False)
    media_name = Column(String, nullable=False)
    media_url = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")


class Keystore(Base):
    __tablename__ = "keystore"
    aid = Column(Integer, Sequence("aid_seq"), primary_key=True)
    keyid = Column(Integer, Sequence("keyid_seq"), primary_key=True)
    init_key = Column(String(250), nullable=False)
    initkey_validation = Column(Boolean, default=False)
    pem_priv = Column(String(250), nullable=True)
    pem_pub = Column(String(250), nullable=True)

    __table_args__ = (PrimaryKeyConstraint("aid", "keyid", name="keystore_pk"),)