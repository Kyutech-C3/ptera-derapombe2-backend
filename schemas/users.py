from typing import Any
import strawberry
from datetime import datetime
from db.models import Color, User

ColorType: Any = strawberry.enum(Color, name="Color")

@strawberry.type(name="User")
class UserType:
	id: str
	name: str
	group: ColorType
	exp_point: int
	level: int
	avatar_number: int
	created_at: datetime
	updated_at: datetime

	@classmethod
	def from_instance(cls, instance: User) -> "UserType":
		data = instance.__dict__
		del data['_sa_instance_state']
		return cls(**data)

@strawberry.input
class AddUserInput:
	name: str
	group: ColorType
	avatar_number: int
