import strawberry
from db.models import Item
from schemas.general import ItemEffectType

@strawberry.type(name="Item")
class ItemType:
	id: str
	name: str
	level: int
	effect: ItemEffectType
	value: float

	@classmethod
	def from_instance(cls, instance: Item) -> "ItemType":
		return cls(
			id=instance.id,
			name=instance.name,
			level=instance.level,
			effect=instance.effect,
			value=instance.value
		)
