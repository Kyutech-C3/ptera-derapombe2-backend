import strawberry
from schemas.general import ItemEffectType

@strawberry.type(name="Item")
class ItemType:
	id: str
	name: str
	level: int
	effect: ItemEffectType
	value: float
	quantity: int

@strawberry.type
class ItemResult:
	item: ItemType
	number_of_acquisition: int
