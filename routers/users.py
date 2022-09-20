from datetime import datetime
import cruds.users as cu
from db.database import get_db
from routers.utils import verify_token
from schemas.users import ColorType, UserType
from strawberry.types import Info

def get_me(info: Info) -> UserType:
	db = next(get_db())
	user_id = verify_token(info)
	me = cu.get_user_by_id(db, user_id)
	return me

def add_user(name: str, group: ColorType, info: Info) -> UserType:
	db = next(get_db())
	user_id = verify_token(info)
	user = cu.create_user(db, user_id, name, group)
	return UserType.from_instance(user)

def update_user(name: str) -> UserType:
	return UserType(
		id='12345',
		name=name,
		group=ColorType.RED,
		exp_point=0,
		level=1,
		created_at=datetime.now(),
		updated_at=datetime.now()
	)
