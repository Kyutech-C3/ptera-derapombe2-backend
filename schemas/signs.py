from datetime import datetime
import strawberry
from db.models import Sign, SignStatus
from schemas.general import ColorType
from schemas.items import ItemResult, ItemType
from schemas.users import UserType

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
	group: ColorType
	hit_point: int
	owner: UserType
	items: list[ItemType]

	@classmethod
	def from_instance(cls, sign_instance: Sign, sign_status_instance: SignStatus) -> "SignType":
		return cls(
			id=sign_instance.id,
			base_sign_types=[bs.type for bs in sign_instance.base_signs],
			longitude=sign_instance.longitude,
			latitude=sign_instance.latitude,
			image_path=sign_instance.image_path,
			max_hit_point=sign_instance.max_hit_point,
			max_link_slot=sign_instance.max_link_slot,
			max_item_slot=sign_instance.max_item_slot,
			group=sign_status_instance.user.group,
			hit_point=sign_status_instance.hit_point,
			owner=UserType.from_instance(sign_status_instance.user),
			items=[ItemType.from_instance(i) for i in sign_status_instance.items]
		)

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
