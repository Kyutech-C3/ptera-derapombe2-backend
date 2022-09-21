from typing import Dict
from sqlalchemy.orm.session import Session
from cruds.users import get_user_by_id
from db.models import BaseSign, BelongSign, GallerySign, Sign, SignStatus

from schemas.signs import Gallery, SignInfo, SignType

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
		max_item_slot=8,
		max_link_slot=12,
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

def get_user_galleries(db: Session, user_id: str) -> list[Gallery]:
	gallery_signs = db.query(GallerySign).filter(GallerySign.user_id == user_id).all()
	temp_dict: Dict[str, list[SignInfo]] = {}
	for gallery in gallery_signs:
		for base_sign in gallery.sign.base_signs:
			if temp_dict.get(str(base_sign.type)) is None:
				temp_dict[str(base_sign)] = [SignInfo.from_instance(gallery.sign)]
			else:
				temp_dict[str(base_sign)].append(SignInfo.from_instance(gallery.sign))

	signs_list = list(temp_dict.items())
	galleries = []
	for i, key in enumerate(list(temp_dict.keys())):
		galleries.append(Gallery(
			base_sign_type=int(key),
			sign=signs_list[i]
		))

	return galleries
