from sqlalchemy.orm import Session
from cruds.users import get_user_by_id
from cruds.signs import get_sign_by_id
from db.models import HavingItem, ItemEffect, SignStatus, UsingItem
from schemas.general import ItemEffectType
from schemas.items import ItemType
from schemas.signs import UpdateSignData

def get_attached_item(db: Session, sign_id: str) -> list[ItemType]:
	attached_items = db.query(UsingItem).filter(UsingItem.sign_id == sign_id).all()

	return [ItemType.from_instance(ai.item) for ai in attached_items]

def attach_item(db: Session, user_id: str, item_id: str, sign_id: str) -> list[ItemType]:
	get_user_by_id(db, user_id)
	sign = get_sign_by_id(db, sign_id)

	using_item_slot = db.query(UsingItem).filter(UsingItem.sign_id == sign.id).count()
	if using_item_slot < sign.max_item_slot:
		having_item = db.query(HavingItem).filter(HavingItem.item_id == item_id, HavingItem.user_id == user_id).first()
		if having_item is None:
			raise Exception('having_item is not found')
		if having_item.item.effect not in [ItemEffect.ENDURANCE, ItemEffect.RESISTANCE]:
			raise Exception('item effect is invalid')
		db.delete(having_item)
		db.add(UsingItem(
			item_id=item_id,
			sign_id=sign_id
		))
		db.commit()

	return get_attached_item(db, sign_id)

def change_item(db: Session, user_id: str, old_item_id: str, new_item_id: str, sign_id: str) -> list[ItemType]:
	get_user_by_id(db, user_id)
	sign = get_sign_by_id(db, sign_id)

	old_item = db.query(UsingItem).filter(UsingItem.item_id == old_item_id, UsingItem.sign_id == sign_id).first()
	if old_item is None:
		raise Exception('attached_item is not found')
	new_having_item = db.query(HavingItem).filter(HavingItem.item_id == new_item_id, HavingItem.user_id == user_id).first()
	if new_having_item is None:
		raise Exception('having_item is not found')
	if new_having_item.item.effect not in [ItemEffect.ENDURANCE, ItemEffect.RESISTANCE]:
		raise Exception('item effect is invalid')

	db.delete(old_item)
	db.delete(new_having_item)
	db.add(UsingItem(
		item_id=new_item_id,
		sign_id=sign_id
	))
	db.commit()

	if old_item.item.effect == ItemEffect.ENDURANCE:
		changing_sign_status = db.query(SignStatus).get(sign_id)
		max_hp = sign.max_hit_point
		for item in changing_sign_status.items:
			if item.effect == ItemEffect.ENDURANCE:
				max_hp += item.value
		changing_sign_status.hit_point = min(changing_sign_status.hit_point, max_hp)
	db.commit()

	return get_attached_item(db, sign_id)

def delete_item(db: Session, user_id: str, item_id: str, sign_id: str) -> list[ItemType]:
	get_user_by_id(db, user_id)
	get_sign_by_id(db, sign_id)

	item = db.query(UsingItem).filter(UsingItem.item_id == item_id, UsingItem.sign_id == sign_id).first()
	if item is None:
		raise Exception('attached_item is not found')
	db.delete(item)
	db.commit()

	return get_attached_item(db, sign_id)

def update_sign(db: Session, sign_id: str, item_id: str, user_id: str) -> UpdateSignData:
	get_user_by_id(db, user_id)
	sign = get_sign_by_id(db, sign_id)

	item = db.query(HavingItem).filter(HavingItem.item_id == item_id, HavingItem.user_id == user_id).first()
	if item is None:
		raise Exception('having_item is not found')
	if item.effect not in [ItemEffect.ATTACK, ItemEffect.HEAL]:
		raise Exception('item effect is invalid')
	db.delete(item)
	changing_sign = db.query(SignStatus).get(sign_id)
	hit_point_diff = -sign.hit_point

	if item.effect == ItemEffectType.ATTACK:
		attack = item.value
		for sign_item in sign.items:
			if sign_item.effect == ItemEffectType.REGISTANCE:
				attack *= sign_item.value
		changing_sign.hit_point = max(changing_sign.hit_point - attack, 0)
		if changing_sign.hit_point <= 0:
			db.delete(changing_sign)

	elif item.effect == ItemEffectType.HEAL:
		max_hp = sign.max_hit_point
		for sign_item in sign.items:
			if sign_item.effect == ItemEffectType.ENDURANCE:
				max_hp += sign_item.value
		changing_sign.hit_point = min(changing_sign.hit_point + item.value, max_hp)

	hit_point_diff += changing_sign.hit_point
	db.commit()

	return UpdateSignData(
		exp_point=30,
		hit_point_diff=hit_point_diff,
		sign=get_sign_by_id(db, sign_id)
	)
