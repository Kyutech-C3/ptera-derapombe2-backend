from schemas.general import ItemEffectType
from schemas.items import ItemType
from cruds import items as ci
from strawberry.types import Info
from db.database import get_db
from routers.utils import verify_token

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

def get_my_items() -> list[ItemType]:
	return [
		ItemType(
			id='hogehoge',
			name='fugafuga',
			level=1,
			effect=ItemEffectType.HEAL,
			value=20,
		)
	]
