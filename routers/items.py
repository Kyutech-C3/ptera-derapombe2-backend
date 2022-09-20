from schemas.general import ItemEffectType
from schemas.items import ItemType

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

def add_item(having_item_id: str) -> list[ItemType]:
	return [
		ItemType(
			id='hogehoge',
			name='fugafuga',
			level=1,
			effect=ItemEffectType.HEAL,
			value=20,
		)
	]

def change_item(having_item_id: str, using_item_id: str) -> list[ItemType]:
	return [
		ItemType(
			id='hogehoge',
			name='fugafuga',
			level=1,
			effect=ItemEffectType.HEAL,
			value=20,
		)
	]

def delete_item(using_item_id: str) -> list[ItemType]:
	return [
		ItemType(
			id='hogehoge',
			name='fugafuga',
			level=1,
			effect=ItemEffectType.HEAL,
			value=20,
		)
	]
