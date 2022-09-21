import os
from main import app
from fastapi.testclient import TestClient
import sqlalchemy
import pytest
from sqlalchemy.orm import sessionmaker
import sqlalchemy_utils
from db.database import get_db
from db.models import Base

DATABASE = 'postgresql'
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = 'sign_gress_test'

DATABASE_URL = "{}://{}:{}@{}/{}".format(DATABASE, USER, PASSWORD, HOST, DB_NAME)

client = TestClient(app)

engine = sqlalchemy.create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def use_test_db_fixture():
	"""
	Override get_db with test DB
	get_db関数をテストDBで上書きする
	"""
	if not sqlalchemy_utils.database_exists(DATABASE_URL):
		print('[INFO] CREATE DATABASE')
		sqlalchemy_utils.create_database(DATABASE_URL)

	# Reset test tables
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	def override_get_db():
		try:
			db = SessionLocal()
			yield db
		finally:
			db.close()

	app.dependency_overrides[get_db] = override_get_db
	yield SessionLocal()

@pytest.fixture
def session_for_test():
	"""
	DB Session for test
	"""
	session = SessionLocal()
	yield session

	session.close()
