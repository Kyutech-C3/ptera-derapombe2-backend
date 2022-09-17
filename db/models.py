import dataclasses
import enum
from typing import Any
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Enum, Integer, Float, ForeignKey
from sqlalchemy.sql.sqltypes import String

Base: Any = declarative_base()

def generate_uuid():
    return str(uuid4())

class Color(str, enum.Enum):
    RED = 'red'
    GREEN = 'green'

@dataclasses.dataclass
class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    group = Column(Enum(Color), nullable=False)
    exp_point = Column(Integer, default=0)
    level = Column(Integer, default=1)
    avatar_number = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

@dataclasses.dataclass
class Sign(Base):
    __tablename__ = 'signs'
    id = Column(String, default=generate_uuid, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    image_path = Column(String)
    max_hit_point = Column(Integer, nullable=False)
    max_link_slot = Column(Integer, nullable=False)
    max_item_slot = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

@dataclasses.dataclass
class SignStatus(Base):
    __tablename__ = 'signs'
    sign_id = Column(String, ForeignKey('signs.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    user_id = Column(String, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    hit_point = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
