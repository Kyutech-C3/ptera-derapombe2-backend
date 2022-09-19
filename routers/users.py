import cruds.users as cu
from db.database import get_db
from routers.utils import verify_token
from schemas.users import AddUserInput, UserType
from strawberry.types import Info

def get_user(user_id: str) -> UserType:
	db = next(get_db())
	user = cu.get_user_by_id(db, user_id)
	return UserType.from_instance(user)

def get_me(info: Info) -> UserType:
	db = next(get_db())
	user_id = verify_token(info)
	me = cu.get_user_by_id(db, user_id)
	return me

def add_user(user_input: AddUserInput, info: Info) -> UserType:
	db = next(get_db())
	user_id = verify_token(info)
	user = cu.create_user(db, user_id, **user_input.__dict__)
	return UserType.from_instance(user)
