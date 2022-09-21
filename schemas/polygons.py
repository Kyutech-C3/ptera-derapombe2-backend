from datetime import datetime
import strawberry
from db.models import LinkingSign, Polygon
from schemas.general import ColorType
from schemas.signs import Coordinate, SignType

@strawberry.type()
class Link:
	polygon_id: str
	sign_id: str
	other_sign_id: str
	one_coordinate: SignType
	other_coordinate: Coordinate
	created_at: datetime

	@classmethod
	def from_instance(cls, instance: LinkingSign) -> "Link":
		return cls(
			sign_id=instance.sign_id,
			other_sign_id=instance.other_sign_id,
			polygon_id=instance.polygon_id,
			created_at=instance.created_at
		)

@strawberry.type(name="Polygon")
class PolygonType:
	id: str
	group: ColorType
	surface: float
	sign_ids: list[str]
	coordinates: list[Coordinate]
	created_at: datetime

	@classmethod
	def from_instance(cls, instance: Polygon) -> "PolygonType":
		sign_ids = []
		for link in instance.links:
			sign_ids.extend([link.sign_id, link.other_sign_id])
		return cls(
			id=instance.id,
			group=instance.group,
			surface=instance.surface,
			sign_ids=set(sign_ids),
			created_at=instance.created_at
		)

@strawberry.type()
class MapInfo:
	signs: list[SignType]
	links: list[Link]
	polygons: list[PolygonType]

@strawberry.type()
class PowerRatio:
	red: float
	green: float
