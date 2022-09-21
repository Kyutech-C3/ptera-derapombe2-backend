from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from cruds.users import get_user_by_id
from cruds.signs import get_sign_by_id
from db.models import LinkingSign, Polygon, Sign
from schemas.polygons import Link, MapInfo, PolygonType
from schemas.signs import SignType

LENGTH_MATER = 30
LENGTH_DEGREE = LENGTH_MATER * 90 / 10000

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

	if abs(sign.longitude - other_sign.longitude) > LENGTH_DEGREE or abs(sign.latitude - other_sign.latitude) > LENGTH_DEGREE:
		raise Exception('too long distance between two signs')

	if not (sign.group == user.group and other_sign.group == user.group):
		raise Exception('you can link only your group Sign')

	min_latitude = min(sign.latitude, other_sign.latitude)
	max_latitude = max(sign.latitude, other_sign.latitude)
	min_longitude = min(sign.longitude, other_sign.longitude)
	max_longitude = max(sign.longitude, other_sign.longitude)

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
		other_sign_id=other_sign_id
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

		# 面積確認
		surface = 100

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
