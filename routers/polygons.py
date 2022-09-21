from datetime import datetime
from db.models import ItemEffect
from schemas.general import ColorType
from schemas.items import ItemType
from schemas.polygons import MapInfo, PolygonType, PowerRatio, Link, Coordinate
from schemas.signs import SignType
from schemas.users import UserType
from cruds import polygons as cp
from strawberry.types import Info
from db.database import get_db
from routers.utils import verify_token

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

def get_map_info() -> MapInfo:
	return MapInfo(
		signs=[
			SignType(
				link_num=2,
				id='11111111111',
				base_sign_types=[1],
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
					ItemType(
						id='item34r5tyujytr4',
						name='耐久アップⅠ',
						level=1,
						effect=ItemEffect.ENDURANCE,
						value=10
					),
					ItemType(
						id='item34r5tyujytr4',
						name='耐久アップⅠ',
						level=1,
						effect=ItemEffect.ENDURANCE,
						value=10
					),
					ItemType(
						id='item34r5tyujytr4345',
						name='耐久アップⅡ',
						level=2,
						effect=ItemEffect.ENDURANCE,
						value=30
					),
				]
			),
			SignType(
				link_num=2,
				id='2222222222',
				base_sign_types=[1],
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
					ItemType(
						id='item34r5tyujytr4',
						name='耐久アップⅠ',
						level=1,
						effect=ItemEffect.ENDURANCE,
						value=10
					),
					ItemType(
						id='item34r52345tyujytr4',
						name='攻撃耐性Ⅰ',
						level=1,
						effect=ItemEffect.RESISTANCE,
						value=0.9
					),
					ItemType(
						id='234567',
						name='攻撃耐性Ⅲ',
						level=3,
						effect=ItemEffect.RESISTANCE,
						value=0.75
					),
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
				base_sign_types=[1],
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
					ItemType(
						id='item34r52345tyujytr4',
						name='攻撃耐性Ⅰ',
						level=1,
						effect=ItemEffect.RESISTANCE,
						value=0.9
					),
					ItemType(
						id='234567',
						name='攻撃耐性Ⅲ',
						level=3,
						effect=ItemEffect.RESISTANCE,
						value=0.75
					),
				]
			),
			SignType(
				link_num=0,
				id='3333333333333344',
				base_sign_types=[1],
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
					ItemType(
						id='item34r5tyujytr4',
						name='耐久アップⅠ',
						level=1,
						effect=ItemEffect.ENDURANCE,
						value=10
					),
					ItemType(
						id='item34r5tyujytr4345',
						name='耐久アップⅡ',
						level=2,
						effect=ItemEffect.ENDURANCE,
						value=30
					),
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
