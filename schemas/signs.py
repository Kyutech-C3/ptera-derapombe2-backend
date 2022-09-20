from datetime import datetime
import strawberry
from db.models import Sign, SignStatus
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

	@classmethod
	def from_instance(cls, instance: Sign) -> "SignInfo":
		data = instance.__dict__
		del data['_sa_instance_state']
		return cls(**data)

@strawberry.type(name="Sign")
class SignType:
	id: str
	base_sign_types: list[int]
	longitude: float
	latitude: float
	image_path: str
	max_hit_point: int
	max_link_slot: int
	max_item_slot: int
	created_at: datetime
	group: ColorType
	hit_point: int
	items: list[ItemType]

	@classmethod
	def from_instance(cls, sign_instance: Sign, sign_status_instance: SignStatus) -> "SignType":
		sign_data = sign_instance.__dict__
		del sign_data['_sa_instance_state']
		sign_status_data = sign_status_instance.__dict__
		del sign_status_data['_sa_instance_state']
		return cls(**sign_data, **sign_status_data)

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

@strawberry.input()
class RegistSignInput:
	base_sign_types: list[int]
	longitude: float
	latitude: float
	image_path: str
