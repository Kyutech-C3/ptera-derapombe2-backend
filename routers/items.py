from schemas.general import ItemEffectType
from schemas.items import ItemType
from cruds import items as ci
from strawberry.types import Info
from db.database import get_db
from routers.utils import verify_token
from schemas.signs import UpdateSignData

def attach_item(sign_id: str, item_id: str, info: Info) -> list[ItemType]:
	db = next(get_db())
	user_id = verify_token(info)

	attached_items = ci.attach_item(db, user_id, item_id, sign_id)

	return attached_items

def change_item(sign_id: str, old_item_id: str, new_item_id: str, info: Info) -> list[ItemType]:
	db = next(get_db())
	user_id = verify_token(info)

	attached_items = ci.change_item(db, user_id, old_item_id, new_item_id, sign_id)

	return attached_items

def delete_item(sign_id: str, item_id: str, info: Info) -> list[ItemType]:
	db = next(get_db())
	user_id = verify_token(info)

	attached_items = ci.delete_item(db, user_id, item_id, sign_id)

	return attached_items

def update_sign(sign_id: str, item_id: str, info: Info) -> UpdateSignData:
	db = next(get_db())
	user_id = verify_token(info)

	updated_sign_data = ci.update_sign(db, sign_id, item_id, user_id)

	return updated_sign_data

def get_my_items(info: Info) -> list[ItemType]:
	db = next(get_db())
	user_id = verify_token(info)

	my_items = ci.get_user_items(db, user_id)

	return my_items
