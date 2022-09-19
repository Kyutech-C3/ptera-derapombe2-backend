from datetime import datetime
import strawberry
from schemas.general import ColorType
from schemas.signs import SignType

@strawberry.type()
class Segment:
	id: str
	sign_id: str
	other_sign_id: str
	created_at: datetime

@strawberry.type(name="Polygon")
class PolygonType:
	id: str
	group: ColorType
	surface: float
	sign_ids: list[str]
	created_at: datetime

@strawberry.type()
class MapInfo:
	signs: list[SignType]
	segments: list[Segment]
	polygons: list[PolygonType]

@strawberry.type()
class PowerRatio:
	red: float
	green: float
