import strawberry
from datetime import datetime
from db.models import User
from .general import ColorType

@strawberry.type(name="User")
class UserType:
	id: str
	name: str
	group: ColorType
	exp_point: int
	level: int
	created_at: datetime
	updated_at: datetime

	@classmethod
	def from_instance(cls, instance: User) -> "UserType":
		data = instance.__dict__
		del data['_sa_instance_state']
		return cls(**data)
