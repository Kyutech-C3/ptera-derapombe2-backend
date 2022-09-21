from datetime import datetime
from typing import Optional
import strawberry
from db.models import Sign, SignStatus
from schemas.general import ColorType
from schemas.items import ItemType
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
	def from_instance(cls, sign_instance: Sign, _: SignStatus = None) -> "SignType":
		return cls(
			id=sign_instance.id,
			base_sign_types=[bs.type for bs in sign_instance.base_signs],
			longitude=sign_instance.longitude,
			latitude=sign_instance.latitude,
			image_path=sign_instance.image_path,
			max_hit_point=sign_instance.max_hit_point,
			max_link_slot=sign_instance.max_link_slot,
			max_item_slot=sign_instance.max_item_slot,
			created_at=sign_instance.created_at
		)

@strawberry.type(name="Sign")
class SignType(SignInfo):
	group: Optional[ColorType]
	hit_point: Optional[int]
	owner: Optional[UserType]
	items: Optional[list[ItemType]]

	@classmethod
	def from_instance(cls, sign_instance: Sign, sign_status_instance: SignStatus = None) -> "SignType":
		return cls(
			id=sign_instance.id,
			base_sign_types=[bs.type for bs in sign_instance.base_signs],
			longitude=sign_instance.longitude,
			latitude=sign_instance.latitude,
			image_path=sign_instance.image_path,
			max_hit_point=sign_instance.max_hit_point,
			max_link_slot=sign_instance.max_link_slot,
			max_item_slot=sign_instance.max_item_slot,
			created_at=sign_instance.created_at,
			group=sign_status_instance.user.group if sign_status_instance is not None else None,
			hit_point=sign_status_instance.hit_point if sign_status_instance is not None else None,
			owner=UserType.from_instance(sign_status_instance.user) if sign_status_instance is not None else None,
			items=[ItemType.from_instance(i) for i in sign_status_instance.items] if sign_status_instance is not None else None
		)

@strawberry.type()
class Gallery:
	base_sign_type: int
	sign: list[SignInfo]

@strawberry.type()
class ExhumeResult:
	items: list[ItemType]
	exp_point: int

@strawberry.type()
class UpdateSignData:
	exp_point: int
	hit_point_diff: int
	sign: SignType

@strawberry.input()
class RegistSignInput:
	base_sign_types: list[int]
	longitude: float
	latitude: float
	image_path: str
