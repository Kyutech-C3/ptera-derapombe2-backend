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
		data = instance.__dict__
		del data['_sa_instance_state']
		return cls(**data)
