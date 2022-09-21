from datetime import datetime
from typing import Optional
import strawberry
from db.models import BaseSign, Sign, SignStatus
from schemas.general import ColorType
from schemas.items import ItemType
from schemas.users import UserType

@strawberry.type()
class Coordinate:
	longitude: float
	latitude: float
	def __init__(self, longitude: float, latitude: float):
		self.longitude = longitude
		self.latitude = latitude

@strawberry.input
class CoordinateInput:
	longitude: float
	latitude: float

@strawberry.type(name="BaseSign")
class BaseSignType:
	id: str
	type: int
	name: str

	@classmethod
	def from_instance(cls, instance: BaseSign) -> "BaseSignType":
		return cls(
			id=instance.id,
			type=instance.type,
			name=instance.name
		)

@strawberry.type()
class SignInfo:
	id: str
	base_signs: list[BaseSignType]
	coordinate: Coordinate
	image_path: str
	max_hit_point: int
	max_link_slot: int
	max_item_slot: int
	created_at: datetime

	@classmethod
	def from_instance(cls, sign_instance: Sign, _: SignStatus = None) -> "SignInfo":
		return cls(
			id=sign_instance.id,
			base_signs=[BaseSignType.from_instance(bs) for bs in sign_instance.base_signs],
			coordinate=Coordinate(
				longitude=sign_instance.longitude,
				latitude=sign_instance.latitude,
			),
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
	link_num: int

	@classmethod
	def from_instance(cls, sign_instance: Sign, sign_status_instance: SignStatus = None) -> "SignType":
		owner: UserType = None
		if sign_status_instance is not None:
			owner = UserType.from_instance(sign_status_instance.user)
		return cls(
			id=sign_instance.id,
			base_signs=[BaseSignType.from_instance(bs) for bs in sign_instance.base_signs],
			coordinate=Coordinate(
				longitude=sign_instance.longitude,
				latitude=sign_instance.latitude,
			),
			image_path=sign_instance.image_path,
			max_hit_point=sign_instance.max_hit_point,
			max_link_slot=sign_instance.max_link_slot,
			max_item_slot=sign_instance.max_item_slot,
			created_at=sign_instance.created_at,
			hit_point=sign_status_instance.hit_point if sign_status_instance is not None else None,
			owner=owner,
			group=owner.group if sign_status_instance is not None else None,
			items=[ItemType.from_instance(i) for i in sign_status_instance.items] if sign_status_instance is not None else None,
			link_num=len(sign_instance.links)
		)

@strawberry.type()
class Gallery:
	base_sign: BaseSignType
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
	coordinate: CoordinateInput
	image_path: str

@strawberry.type
class NearlySign:
	distanse: float
	sign: SignType
