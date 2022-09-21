from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from db.models import LinkingSign, Polygon, Sign, Color, SignStatus
from cruds.users import get_user_by_id
from cruds.signs import get_sign_by_id
from schemas.polygons import Link, MapInfo, PolygonType, PowerRatio
from schemas.signs import Coordinate, SignType
from shapely.geometry import shape
from shapely.ops import transform
import pyproj
from functools import partial

LENGTH_KILO_MATER = 10
LENGTH_DEGREE = LENGTH_KILO_MATER * 90 / 10000

def calc_power_ratio(db: Session):
	red_surface = db.query(func.sum(Polygon.surface)).filter(Polygon.group == Color.RED).group_by(Polygon.group).first()
	if red_surface is None:
		red_surface = 0
	green_surface = db.query(func.sum(Polygon.surface)).filter(Polygon.group == Color.GREEN).group_by(Polygon.group).first()
	if green_surface is None:
		green_surface = 0

	return PowerRatio(
		red=red_surface/(red_surface+green_surface) if (red_surface+green_surface) > 0 else 0.5,
		green=green_surface/(red_surface+green_surface) if (red_surface+green_surface) > 0 else 0.5
	)


def create_link(db: Session, sign_id: str, other_sign_id: str, user_id: str):
	user = get_user_by_id(db, user_id)
	sign = get_sign_by_id(db, sign_id)
	other_sign = get_sign_by_id(db, other_sign_id)
	link = db.query(LinkingSign).filter(or_(
		and_(LinkingSign.sign_id == sign_id, LinkingSign.other_sign_id == other_sign_id),
		and_(LinkingSign.sign_id == other_sign_id, LinkingSign.other_sign_id == sign_id)
	)).first()
	if link is not None:
		raise Exception('this link is already exist')

	link_count = db.query(LinkingSign).filter(or_(LinkingSign.sign_id == sign_id, LinkingSign.other_sign_id == sign_id)).count()
	other_link_count = db.query(LinkingSign).filter(or_(LinkingSign.sign_id == other_sign_id, LinkingSign.other_sign_id == other_sign_id)).count()

	# TODO 決め打ちを修正する
	max_link_slot = 2

	if link_count >= max_link_slot or other_link_count >= max_link_slot:
		raise Exception('these signs\' link slot is not empty')

	if abs(sign.coordinate.longitude - other_sign.coordinate.longitude) > LENGTH_DEGREE or abs(sign.coordinate.latitude - other_sign.coordinate.latitude) > LENGTH_DEGREE:
		raise Exception('too long distance between two signs')

	if not (sign.group == user.group and other_sign.group == user.group):
		raise Exception('you can link only your group Sign')

	min_latitude = min(sign.coordinate.latitude, other_sign.coordinate.latitude)
	max_latitude = max(sign.coordinate.latitude, other_sign.coordinate.latitude)
	min_longitude = min(sign.coordinate.longitude, other_sign.coordinate.longitude)
	max_longitude = max(sign.coordinate.longitude, other_sign.coordinate.longitude)

	nearly_signs = db.query(Sign).filter(
		min_latitude - LENGTH_DEGREE < Sign.latitude,
		max_latitude + LENGTH_DEGREE > Sign.latitude,
		min_longitude - LENGTH_DEGREE < Sign.longitude,
		max_longitude + LENGTH_DEGREE < Sign.longitude,
	).all()

	nearly_sign_ids = [nearly_sign.id for nearly_sign in nearly_signs]

	nearly_links = db.query(LinkingSign).filter(LinkingSign.sign_id.in_(nearly_sign_ids), LinkingSign.other_sign_id.in_(nearly_sign_ids)).all()

	for nearly_link in nearly_links:
		near_sign = get_sign_by_id(db, nearly_link.sign_id)
		near_other_sign = get_sign_by_id(db, nearly_link.other_sign_id)
		if cross_check(sign, other_sign, near_sign, near_other_sign):
			raise Exception('link is crossing')

	link = LinkingSign(
		sign_id=sign_id,
		other_sign_id=other_sign_id,
		group=user.group
	)
	db.add(link)
	db.commit()
	db.refresh(link)

	update_signs = [sign, other_sign]
	update_links = [link]
	polygons = []

	data = recursion(db, link.other_sign_id, link.sign_id, link.other_sign_id)
	if data is None:
		data = recursion(db, link.sign_id, link.other_sign_id, link.sign_id)

	if data is not None:
		update_signs = [get_sign_by_id(db, sign_id) for sign_id in data['polygon_signs']]
		update_links = data['polygon_links']

		geom = shape({'type': 'Polygon', 'coordinates': [[[update_sign.coordinate.longitude, update_sign.coordinate.latitude] for update_sign in update_signs]]})
		swapped_geom = swap_xy(geom)
		project = partial(
			pyproj.transform,
			pyproj.CRS.from_epsg(4326),
			pyproj.CRS.from_epsg(3410))
		trans = transform(project, swapped_geom)

		surface = trans.area

		polygon = Polygon(
			group=user.group,
			surface=surface,
		)
		db.add(polygon)
		db.commit()
		db.refresh(polygon)

		for link in data['polygon_links']:
			link.polygon_id = polygon.id
		db.commit()
		polygons.append(polygon)

	return MapInfo(
		signs=update_signs,
		links=[Link.from_instance(update_link) for update_link in update_links],
		polygons=[PolygonType.from_instance(polygon) for polygon in polygons]
	)

def recursion(db: Session, goal_id: str, star_id: str, base_id: str):
	links = db.query(LinkingSign).filter(or_(LinkingSign.sign_id == star_id, LinkingSign.other_sign_id == star_id)).all()
	for link in links:
		if link.sign_id != base_id and link.other_sign_id != base_id:
			next_sign_id = link.sign_id if link.other_sign_id == star_id else link.other_sign_id
			if next_sign_id == goal_id:
				return {
					'polygon_signs': [goal_id],
					'polygon_links': [link],
				}
			else:
				data = recursion(db, goal_id, next_sign_id, star_id)
				if data is not None:
					data['polygon_signs'].append(next_sign_id)
					data['polygon_links'].append(link)
				return data
	return None

def cross_check(one_start: SignType, one_end: SignType, other_start: SignType, other_end: SignType) -> bool:
	s = (one_start.longitude - one_end.longitude) * (other_start.latitude - one_start.latitude) - (one_start.latitude - one_end.latitude) * (other_start.longitude - one_start.longitude);
	t = (one_start.longitude - one_end.longitude) * (other_end.latitude - one_start.latitude) - (one_start.latitude - one_end.latitude) * (other_end.longitude - one_start.longitude);
	if s * t > 0:
		return False

	s = (other_start.longitude - other_end.longitude) * (one_start.latitude - other_start.latitude) - (other_start.latitude - other_end.latitude) * (one_start.longitude - other_start.longitude);
	t = (other_start.longitude - other_end.longitude) * (one_end.latitude - other_start.latitude) - (other_start.latitude - other_end.latitude) * (one_end.longitude - other_start.longitude);
	if s * t > 0:
		return False
	return True

def swap_xy(geom):
    # (x, y) -> (y, x)
    def swap_xy_coords(coords):
        for x, y in coords:
            yield (y, x)

    # if geom.type == 'Polygon':
    def swap_polygon(geom):
        ring = geom.exterior
        shell = type(ring)(list(swap_xy_coords(ring.coords)))
        holes = list(geom.interiors)
        for pos, ring in enumerate(holes):
            holes[pos] = type(ring)(list(swap_xy_coords(ring.coords)))
        return type(geom)(shell, holes)

    # if geom.type == 'MultiPolygon':
    def swap_multipolygon(geom):
        return type(geom)([swap_polygon(part) for part in geom.geoms])

    # Main
    if geom.type == 'Polygon':
        return swap_polygon(geom)
    elif geom.type == 'MultiPolygon':
        return swap_multipolygon(geom)
    else:
        raise TypeError('Unexpected geom.type:', geom.type)

def get_map_info(db: Session, min_coordinate: Coordinate, max_coordinate: Coordinate):
	map_signs = []
	signs = db.query(Sign).filter(
		Sign.latitude > min_coordinate.latitude,
		Sign.latitude < max_coordinate.latitude,
		Sign.longitude > min_coordinate.longitude,
		Sign.longitude < max_coordinate.longitude
	).all()
	for sign in signs:
		sign_status = db.query(SignStatus).filter(SignStatus.sign_id == sign.id).first()
		map_signs.append(SignType.from_instance(sign, sign_status))

	linking = db.query(LinkingSign).filter(or_(LinkingSign.sign.in_(signs), LinkingSign.other_sign.in_(signs))).all()
	polygon_ids: List[str] = []
	for link in linking:
		if link.polygon_id is not None:
			polygon_ids.append(link.polygon_id)
	polygon_ids = set(polygon_ids)
	polygons = db.query(Polygon).filter(Polygon.id.in_(polygon_ids)).all()
	return MapInfo(
		signs=map_signs,
		links=[Link.from_instance(link) for link in linking],
		polygons=[PolygonType.from_instance(polygon) for polygon in polygons]
	)
