import dataclasses
import enum
from typing import Any
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Enum
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
    id = Column(String, default=generate_uuid, primary_key=True, index=True)
    name = Column(String, unique=False, index=True, nullable=False)
    group = Column(Enum(Color), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
