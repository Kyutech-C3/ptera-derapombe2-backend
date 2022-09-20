from datetime import datetime
import strawberry
from schemas.general import ColorType
from schemas.items import ItemResult, ItemType

@strawberry.type()
class SignInfo:
	id: str
	base_sign_types: list[int]
	longitude: float
	latitude: float
	image_path: str
	max_hit_point: int
	max_link_slot: int
	max_item_slot: int
	created_at: datetime

@strawberry.type(name="Sign")
class SignType(SignInfo):
	group: ColorType
	hit_point: int
	items: list[ItemType]

@strawberry.type()
class Gallery:
	base_sign_type: int
	sign: list[SignInfo]

@strawberry.type()
class ExhumeResult:
	get_exp_point: int
	get_items: list[ItemResult]

@strawberry.type()
class AttackResult:
	items: list[ItemType]
	get_exp_point: int
	loss_hit_point: int
