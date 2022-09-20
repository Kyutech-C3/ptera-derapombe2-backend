import dataclasses
import enum
from typing import Any
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column as Col, DateTime, Enum, Integer, Float, ForeignKey
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.orm import relationship

Base: Any = declarative_base()

# nullableをdefaultでFalseにするクラス
class Column(Col):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('nullable', False)
        super().__init__(*args, **kwargs)

class Color(str, enum.Enum):
    RED = 'red'
    GREEN = 'green'

class ItemEffect(str, enum.Enum):
    ENDURANCE = 'endurance'  # 耐久アップ(HPアップ)
    RESISTANCE = 'resistance'  # 攻撃耐性アップ(ダメージ量軽減)
    HEAL = 'heal'  # 回復
    ATTACK = 'attack'  # 攻撃

def generate_uuid():
    return str(uuid4())

@dataclasses.dataclass
class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String, unique=False)
    group = Column(Enum(Color))
    exp_point = Column(Integer, default=0)
    level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

@dataclasses.dataclass
class Sign(Base):
    __tablename__ = 'signs'
    id = Column(String, default=generate_uuid, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    image_path = Column(String)
    max_hit_point = Column(Integer)
    max_link_slot = Column(Integer)
    max_item_slot = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    base_signs = relationship("BaseSign", secondary="belong_signs")

@dataclasses.dataclass
class SignStatus(Base):
    __tablename__ = 'sign_statuses'
    sign_id = Column(String, ForeignKey('signs.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    user_id = Column(String, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    hit_point = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    items = relationship("UsingItem")
    user = relationship("User")

@dataclasses.dataclass
class Item(Base):
    __tablename__ = 'items'
    id = Column(String, default=generate_uuid, primary_key=True)
    name = Column(String, unique=False)
    level = Column(Integer)
    effect = Column(Enum(ItemEffect))
    value = Column(Float)

@dataclasses.dataclass
class Polygon(Base):
    __tablename__ = 'polygons'
    id = Column(String, default=generate_uuid, primary_key=True)
    group = Column(Enum(Color))
    surface = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

@dataclasses.dataclass
class LinkingSign(Base):
    __tablename__ = 'linking_signs'
    sign_id = Column(String, ForeignKey('signs.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    other_sign_id = Column(String, ForeignKey('signs.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    polygon_id = Column(String, ForeignKey('polygons.id', onupdate='CASCADE', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

@dataclasses.dataclass
class GallerySign(Base):
    __tablename__ = 'gallery_signs'
    id = Column(String, default=generate_uuid, primary_key=True)
    sign_id = Column(String, ForeignKey('signs.id', onupdate='CASCADE', ondelete='CASCADE'))
    user_id = Column(String, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.now)

@dataclasses.dataclass
class HavingItem(Base):
    __tablename__ = 'having_items'
    id = Column(String, default=generate_uuid, primary_key=True)
    item_id = Column(String, ForeignKey('items.id', onupdate='CASCADE', ondelete='CASCADE'))
    user_id = Column(String, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.now)

@dataclasses.dataclass
class UsingItem(Base):
    __tablename__ = 'using_items'
    id = Column(String, default=generate_uuid, primary_key=True)
    item_id = Column(String, ForeignKey('items.id', onupdate='CASCADE', ondelete='CASCADE'))
    sign_id = Column(String, ForeignKey('sign_statuses.sign_id', onupdate='CASCADE', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.now)

@dataclasses.dataclass
class BaseSign(Base):
    __tablename__ = 'base_signs'
    id = Column(String, default=generate_uuid, primary_key=True)
    type = Column(Integer)

@dataclasses.dataclass
class BelongSign(Base):
    __tablename__ = 'belong_signs'
    sign_id = Column(String, ForeignKey('signs.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    base_sign_id = Column(String, ForeignKey('base_signs.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
