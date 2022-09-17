import os
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE = 'postgresql'
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = os.environ.get('POSTGRES_DB')

SQLALCHEMY_DATABASE_URL = f'{DATABASE}://{USER}:{PASSWORD}@{HOST}/{DB_NAME}'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
