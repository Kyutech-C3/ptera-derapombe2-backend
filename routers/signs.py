from datetime import datetime
from strawberry.file_uploads import Upload
from schemas.general import ColorType, ItemEffectType
from schemas.items import ItemType
from schemas.predict import PredictResult, SuggestResult
from schemas.signs import ExhumeResult, Gallery, RegistSignInput, SignInfo, SignType
from cruds import signs as cs
from strawberry.types import Info
from db.database import get_db
from routers.utils import verify_token

def regist_sign(regist_sign_input: RegistSignInput, info: Info) -> SignType:
	db = next(get_db())
	user_id = verify_token(info)
	new_sign = cs.regist_sign(
		db, user_id, regist_sign_input.base_sign_types,
		regist_sign_input.longitude,
		regist_sign_input.latitude,
		regist_sign_input.image_path
	)
	return new_sign

def get_sign(sign_id: str) -> SignType:
	return SignType(
		id=sign_id,
		base_sign_types=[1],
		longitude=130.671892,
		latitude=33.654921,
		image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
		max_hit_point=100,
		max_item_slot=8,
		max_link_slot=12,
		created_at=datetime.now(),
		group=ColorType.RED,
		hit_point=25,
		items=[ItemType(
			id='12341234',
			name='攻撃耐性Ⅲ',
			level=3,
			effect=ItemEffectType.RESISTANCE,
			value=0.75,
			quantity=4
		)]
	)

def get_my_galleries() -> list[Gallery]:
	return [
		Gallery(
			base_sign_type=23,
			sign=[
				SignInfo(
					id='hoge',
					base_sign_types=[1, 23],
					longitude=130.671892,
					latitude=33.654921,
					image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
					max_hit_point=100,
					max_item_slot=8,
					max_link_slot=12,
					created_at=datetime.now()
				)
			]
		)
	]

def capture_sign(sign_id: str) -> SignType:
	return SignType(
		id=sign_id,
		base_sign_types=[1],
		longitude=130.671892,
		latitude=33.654921,
		image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
		max_hit_point=100,
		max_item_slot=8,
		max_link_slot=12,
		created_at=datetime.now(),
		group=ColorType.RED,
		hit_point=25,
		items=[ItemType(
			id='12341234',
			name='攻撃耐性Ⅲ',
			level=3,
			effect=ItemEffectType.RESISTANCE,
			value=0.75,
			quantity=4
		)]
	)

def exhume_sign(sign_id: str) -> list[ExhumeResult]:
	return [
		ExhumeResult(
			exp_point=1024,
			items=[
				ItemType(
					id='hogehoge',
					name='fugafuga',
					level=1,
					effect=ItemEffectType.HEAL,
					value=20,
					quantity=24
				)
			]
		)
	]

def predict_image(image: Upload) -> PredictResult:
	return PredictResult(
		status=True,
		scores=[
			SuggestResult(
				score=0.9988,
				sign_type=23
			),
			SuggestResult(
				score=0.001,
				sign_type=3
			)
		]
	)
