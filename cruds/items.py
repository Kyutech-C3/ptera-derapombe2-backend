from sqlalchemy.orm import Session
from cruds.users import get_user_by_id
from cruds.signs import get_sign_by_id
from db.models import HavingItem, UsingItem
from schemas.items import ItemType

def get_attached_item(db: Session, sign_id: str) -> list[ItemType]:
	attached_items = db.query(UsingItem).filter(UsingItem.sign_id == sign_id).all()

	return [ItemType.from_instance(ai.item) for ai in attached_items]

def attach_item(db: Session, user_id: str, item_id: str, sign_id: str) -> list[ItemType]:
	get_user_by_id(db, user_id)
	sign = get_sign_by_id(db, sign_id)

	using_item_slot = db.query(UsingItem).filter(UsingItem.sign_id == sign.id).count()
	if using_item_slot < sign.max_item_slot:
		item = db.query(HavingItem).filter(HavingItem.item_id == item_id, HavingItem.user_id == user_id).first()
		if item is None:
			raise Exception('having_item is not found')
		db.delete(item)
		db.add(UsingItem(
			item_id=item_id,
			sign_id=sign_id
		))
		db.commit()

	return get_attached_item(db, sign_id)

def change_item(db: Session, user_id: str, old_item_id: str, new_item_id: str, sign_id: str):
	get_user_by_id(db, user_id)
	get_sign_by_id(db, sign_id)

	old_item = db.query(UsingItem).filter(UsingItem.item_id == old_item_id, UsingItem.sign_id == sign_id).first()
	if old_item is None:
		raise Exception('attached_item is not found')
	new_item = db.query(HavingItem).filter(HavingItem.item_id == new_item_id, HavingItem.user_id == user_id).first()
	if new_item is None:
		raise Exception('having_item is not found')
	db.delete(old_item)
	db.delete(new_item)
	db.add(UsingItem(
		item_id=new_item_id,
		sign_id=sign_id
	))
	db.commit()

	return get_attached_item(db, sign_id)

def delete_item(db: Session, user_id: str, item_id: str, sign_id: str):
	get_user_by_id(db, user_id)
	get_sign_by_id(db, sign_id)

	item = db.query(UsingItem).filter(UsingItem.item_id == item_id, UsingItem.sign_id == sign_id).first()
	if item is None:
		raise Exception('attached_item is not found')
	db.delete(item)
	db.commit()

	return get_attached_item(db, sign_id)
