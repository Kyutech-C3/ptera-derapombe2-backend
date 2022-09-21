from schemas.polygons import MapInfo, PowerRatio, Coordinate
from cruds import polygons as cp
from strawberry.types import Info
from db.database import get_db
from routers.utils import verify_token
from schemas.signs import CoordinateInput

def create_link(sign_id: str, other_sign_id: str, info: Info) -> MapInfo:
	db = next(get_db())
	user_id = verify_token(info)

	updated_map_info = cp.create_link(db, sign_id, other_sign_id, user_id)
	return updated_map_info

def get_power_ratio(info: Info) -> PowerRatio:
	db = next(get_db())
	verify_token(info)
	ratio = cp.calc_power_ratio(db)
	return ratio

def get_map_info(min_coordinate: CoordinateInput, max_coordinate: CoordinateInput, info: Info) -> MapInfo:
	db = next(get_db())
	verify_token(info)
	map_info = cp.get_map_info(db, min_coordinate, max_coordinate)
	return map_info
