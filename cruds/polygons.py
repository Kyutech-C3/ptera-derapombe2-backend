from datetime import datetime
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from db.models import BaseSign, Item, LinkingSign, Polygon, Sign, Color, SignStatus
from cruds.users import get_user_by_id
from cruds.signs import get_sign_by_id
from schemas.general import ColorType
from schemas.polygons import Link, MapInfo, PolygonType, PowerRatio
from schemas.signs import Coordinate, SignType
from shapely.geometry import shape
from shapely.ops import transform
import pyproj
from functools import partial

from schemas.users import UserType

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

def get_map_info(db: Session):
	items = db.query(Item).all()
	base_signs = db.query(BaseSign).all()
	return MapInfo(
		signs=[
			SignType(
				link_num=2,
				id='11111111111',
				base_signs=[
					base_signs[22]
				],
				coordinate=Coordinate(
					latitude=33.88236993479559,
					longitude=130.87800726001615,
				),
				image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
				max_hit_point=100,
				max_item_slot=6,
				max_link_slot=2,
				owner=UserType(
					id='12345',
					name='name',
					group=ColorType.RED,
					exp_point=0,
					avatar_url='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
					level=1,
					created_at=datetime.now(),
					updated_at=datetime.now()
				),
				created_at=datetime.now(),
				group=ColorType.RED, hit_point=24,
				items=[
					items[0],
					items[1],
					items[0],
				]
			),
			SignType(
				link_num=2,
				id='2222222222',
				base_signs=[
					base_signs[22]
				],
				coordinate=Coordinate(
					latitude=33.88240831993862,
					longitude=130.8778279509555,
				),
				image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
				max_hit_point=100,
				max_item_slot=6,
				max_link_slot=2,
				created_at=datetime.now(),
				group=ColorType.RED, hit_point=24, items=[
					items[0],
					items[3],
					items[5],
				],
				owner=UserType(
					id='12345',
					name='name',
					group=ColorType.RED,
					avatar_url='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
					exp_point=0,
					level=1,
					created_at=datetime.now(),
					updated_at=datetime.now()
				),
			),
			SignType(
				link_num=2,
				id='3333333333333333',
				base_signs=[
					base_signs[22]
				],
				owner=UserType(
					id='12345',
					name='name',
					group=ColorType.RED,
					exp_point=0,
					avatar_url='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
					level=1,
					created_at=datetime.now(),
					updated_at=datetime.now()
				),
				coordinate=Coordinate(
					latitude=33.88223979967025,
					longitude=130.87878426594528,
				),
				image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
				max_hit_point=100,
				max_item_slot=6,
				max_link_slot=2,
				created_at=datetime.now(),
				group=ColorType.RED, hit_point=24, items=[
					items[0],
					items[2],
				]
			),
			SignType(
				link_num=0,
				id='3333333333333344',
				base_signs=[
					base_signs[22]
				],
				coordinate=Coordinate(
					latitude=33.88204880963038,
					longitude=130.8784008377654,
				),
				image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
				max_hit_point=100,
				owner=UserType(
					id='12345',
					name='name',
					group=ColorType.GREEN,
					exp_point=0,
					avatar_url='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
					level=1,
					created_at=datetime.now(),
					updated_at=datetime.now()
				),
				max_item_slot=6,
				max_link_slot=2,
				created_at=datetime.now(),
				group=ColorType.GREEN, hit_point=24, items=[
					items[0],
					items[1],
				]
			),
		],
		links=[
			Link(
				polygon_id='88888888',
				group=ColorType.RED,
				sign_id='11111111111',
				other_sign_id='2222222222',
				one_coordinate=Coordinate(
					latitude=33.88236993479559,
					longitude=130.87800726001615,
				),
				other_coordinate=Coordinate(
					latitude=33.88240831993862,
					longitude=130.8778279509555,
				),
				created_at=datetime.now()
			),
			Link(
				polygon_id='88888888',
				group=ColorType.RED,
				sign_id='2222222222',
				other_sign_id='3333333333333333',
				one_coordinate=Coordinate(
					latitude=33.88240831993862,
					longitude=130.8778279509555,
				),
				other_coordinate=Coordinate(
					latitude=33.88223979967025,
					longitude=130.87878426594528,
				),
				created_at=datetime.now()
			),
			Link(
				polygon_id='88888888',
				group=ColorType.RED,
				sign_id='11111111111',
				other_sign_id='3333333333333333',
				one_coordinate=Coordinate(
					latitude=33.88236993479559,
					longitude=130.87800726001615,
				),
				other_coordinate=Coordinate(
					latitude=33.88223979967025,
					longitude=130.87878426594528,
				),
				created_at=datetime.now()
			)
		],
		polygons=[
			PolygonType(
				id='88888888',
				group=ColorType.RED,
				surface=1.2456,
				sign_ids=['11111111111', '2222222222', '3333333333333333'],
				coordinates=[
					Coordinate(
						latitude=33.88236993479559,
						longitude=130.87800726001615,
					),
					Coordinate(
						latitude=33.88240831993862,
						longitude=130.8778279509555,
					),
					Coordinate(
						latitude=33.88223979967025,
						longitude=130.87878426594528,
					),
				],
				created_at=datetime.now()
			)
		]
	)
	# map_signs = []
	# signs = db.query(Sign).all()
	# for sign in signs:
	# 	sign_status = db.query(SignStatus).filter(SignStatus.sign_id == sign.id).first()
	# 	map_signs.append(SignType.from_instance(sign, sign_status))

	# linking = db.query(LinkingSign).all()
	# polygons = db.query(Polygon).all()
	# return MapInfo(
	# 	signs=map_signs,
	# 	links=[Link.from_instance(link) for link in linking],
	# 	polygons=[PolygonType.from_instance(polygon) for polygon in polygons]
	# )
