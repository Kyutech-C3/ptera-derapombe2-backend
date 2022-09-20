from datetime import datetime
from strawberry.file_uploads import Upload
from schemas.general import ColorType, ItemEffectType
from schemas.items import ItemResult, ItemType
from schemas.predict import PredictResult, SuggestResult
from schemas.signs import AttackResult, ExhumeResult, Gallery, RegistSignInput, SignInfo, SignType

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

def regist_sign(regist_sign_input: RegistSignInput) -> SignType:
	return SignType(
		id='hoge',
		base_sign_types=regist_sign_input.base_sign_types,
		longitude=regist_sign_input.longitude,
		latitude=regist_sign_input.latitude,
		image_path=regist_sign_input.image_path,
		max_hit_point=1000,
		max_item_slot=8,
		max_link_slot=12,
		created_at=datetime.now(),
		group=ColorType.RED,
		hit_point=100,
		items=[]
	)

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
			get_exp_point=1024,
			get_items=[
				ItemResult(
					item=ItemType(
						id='hogehoge',
						name='fugafuga',
						level=1,
						effect=ItemEffectType.HEAL,
						value=20,
						quantity=24
					),
					number_of_acquisition=12
				)
			]
		)
	]

def attack_sign(sign_id: str, having_item_id: str) -> AttackResult:
	return AttackResult(
		items=[
			ItemType(
				id='hogehoge',
				name='fugafuga',
				level=1,
				effect=ItemEffectType.HEAL,
				value=20,
				quantity=24
			)
		],
		get_exp_point=1024,
		loss_hit_point=12
	)

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