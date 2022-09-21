from datetime import datetime
from typing import Optional
import strawberry
from db.models import LinkingSign, Polygon
from schemas.general import ColorType
from schemas.signs import Coordinate, SignType

@strawberry.type()
class Link:
	polygon_id: Optional[str]
	group: ColorType
	sign_id: str
	other_sign_id: str
	one_coordinate: Coordinate
	other_coordinate: Coordinate
	created_at: datetime

	@classmethod
	def from_instance(cls, instance: LinkingSign) -> "Link":
		return cls(
			sign_id=instance.sign_id,
			group=instance.group,
			other_sign_id=instance.other_sign_id,
			polygon_id=instance.polygon_id,
			one_coordinate=Coordinate(
				latitude=instance.sign.latitude,
				longitude=instance.sign.longitude),
			other_coordinate=Coordinate(
				latitude=instance.other_sign.latitude,
				longitude=instance.other_sign.longitude),
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
		coordinates = []
		for link in instance.links:
			sign_ids.extend([link.sign_id, link.other_sign_id])
			coordinates.extend([
				Coordinate(
					latitude=link.sign.latitude,
					longitude=link.sign.longitude),
				Coordinate(
					latitude=link.other_sign.latitude,
					longitude=link.other_sign.longitude)
			])
		return cls(
			id=instance.id,
			group=instance.group,
			surface=instance.surface,
			sign_ids=set(sign_ids),
			coordinates=coordinates,
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
