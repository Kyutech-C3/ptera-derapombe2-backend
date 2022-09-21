from tokenize import group
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
	avatar_url: str
	created_at: datetime
	updated_at: datetime

	@classmethod
	def from_instance(cls, instance: User) -> "UserType":
		return cls(
			id=instance.id,
			name=instance.name,
			group=instance.group,
			exp_point=instance.exp_point,
			level=instance.level,
			created_at=instance.created_at,
			updated_at=instance.updated_at
		)
