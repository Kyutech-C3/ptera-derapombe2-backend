from typing import Dict
from sqlalchemy.orm.session import Session
from cruds.users import get_user_by_id
from db.models import BaseSign, BelongSign, GallerySign, HavingItem, Item, Level, Sign, SignStatus
from schemas.items import ItemType
from schemas.signs import BaseSignType, Gallery, NearlySign, SignInfo, ExhumeResult, SignType
import random
from geopy.distance import geodesic

def regist_sign(db: Session, user_id: str, base_sign_types: list[int], longitude: float, latitude: float, image_path: str) -> SignType:
	# TODO 座標が近く，base_sign_typeが一致しているものはすでに登録されていないかと確認する処理もほしいね
	get_user_by_id(db, user_id)

	base_sign_ids = []
	for base_sign_type in base_sign_types:
		base_sign = db.query(BaseSign).filter(BaseSign.type == base_sign_type).first()
		if base_sign is None:
			raise Exception('base_sign is not found')
		base_sign_ids.append(base_sign.id)

	sign = Sign(
		longitude=longitude,
		latitude=latitude,
		image_path=image_path,
		max_hit_point=100,
		max_item_slot=6,
		max_link_slot=2,
	)
	db.add(sign)
	db.commit()
	db.refresh(sign)

	for base_sign_id in base_sign_ids:
		db.add(BelongSign(
			sign_id=sign.id,
			base_sign_id=base_sign_id
		))
	sign_status = SignStatus(
		sign_id=sign.id,
		user_id=user_id,
		hit_point=sign.max_hit_point
	)
	db.add(sign_status)
	gallery_sign = GallerySign(
		sign_id=sign.id,
		user_id=user_id
	)
	db.add(gallery_sign)
	db.commit()
	db.refresh(sign_status)

	registed_sign = SignType.from_instance(sign, sign_status)
	return registed_sign

def get_sign_by_id(db: Session, sign_id: str) -> SignType:
	sign = db.query(Sign).get(sign_id)
	if sign is None:
		raise Exception('sign is not found')
	sign_status = db.query(SignStatus).get(sign_id)
	return SignType.from_instance(sign, sign_status)

def capture_sign(db: Session, sign_id: str, user_id: str) -> SignType:
	sign = db.query(Sign).get(sign_id)
	if sign is None:
		raise Exception('sign_id is invalid')
	sign_status = db.query(SignStatus).get(sign_id)
	if sign_status is not None:
		raise Exception('this sign is already captured')

	sign_status = SignStatus(
		sign_id=sign.id,
		user_id=user_id,
		hit_point=sign.max_hit_point
	)

	db.add(sign_status)
	db.commit()
	db.refresh(sign_status)

	registed_sign = SignType.from_instance(sign, sign_status)
	return registed_sign

def exhume_sign(db: Session, sign_id: str, user_id: str) -> ExhumeResult:
	exp_point = 100
	items = db.query(Item).all()
	exhume_items = random.choices(items, k=random.randint(2, 6))

	user = get_user_by_id(db, user_id)
	user.exp_point += exp_point
	next_border = db.query(Level).get(user.level+1)
	while user.exp_point > next_border.required_exp:
		user.exp_point -= next_border.required_exp
		user.level += 1
		next_border = db.query(Level).get(user.level+1)

	for exhume_item in exhume_items:
		db.add(HavingItem(
			item_id=exhume_item.id,
			user_id=user_id
		))
	db.commit()

	return ExhumeResult(
		items=[ItemType.from_instance(exhume_item) for exhume_item in exhume_items],
		exp_point=exp_point
	)

def get_user_galleries(db: Session, user_id: str) -> list[Gallery]:
	gallery_signs = db.query(GallerySign).filter(GallerySign.user_id == user_id).all()
	temp_dict: Dict[str, list[SignInfo]] = {}
	for gallery in gallery_signs:
		for base_sign in gallery.sign.base_signs:
			if temp_dict.get(str(base_sign.type)) is None:
				temp_dict[str(base_sign.type)] = [
					{
						'base_sign': BaseSignType.from_instance(base_sign),
						'sign': SignInfo.from_instance(gallery.sign)
					}
				]
			else:
				temp_dict[str(base_sign.type)].append({
					'base_sign': BaseSignType.from_instance(base_sign),
					'sign': SignInfo.from_instance(gallery.sign)
				})

	galleries = []
	for i, val in enumerate(list(temp_dict.values())):
		galleries.append(Gallery(
			base_sign=val[i]['base_sign'],
			sign=val[i]['sign']
		))

	return galleries

def get_nearly_signs(db: Session, sign_id: str):
	sign = db.query(Sign).get(sign_id)
	main_coord = (sign.latitude, sign.longitude)

	nearly_signs = []
	candidate_nearly_signs = db.query(Sign).filter(
		Sign.longitude > Sign.longitude - 0.0005,
		Sign.longitude < Sign.longitude + 0.0005,
		Sign.latitude > Sign.latitude - 0.0005,
		Sign.latitude > Sign.latitude + 0.0005,
		).all()

	for nearly_sign in candidate_nearly_signs:
		nearly_coord = (nearly_sign.latitude, sign.longitude)
		dis = geodesic(main_coord, nearly_coord).m
		if dis < 10:
			sign_status = db.query(SignStatus).get(nearly_sign.id)
			nearly_signs.append(NearlySign(
				distanse=dis,
				sign=SignType.from_instance(nearly_sign, sign_status)
			))
	return nearly_signs
