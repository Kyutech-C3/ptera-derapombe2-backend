from datetime import datetime
from schemas.general import ColorType
from schemas.polygons import MapInfo, PolygonType, PowerRatio, Segment
from schemas.signs import SignType

def get_power_ratio() -> PowerRatio:
	return PowerRatio(
		red=65.4,
		green=34.6
	)

def get_map_info() -> MapInfo:
	return MapInfo(
		signs=[
			SignType(
				id='11111111111',
				base_sign_types=[1],
				longitude=130.671892,
				latitude=33.654921,
				image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
				max_hit_point=100,
				max_item_slot=8,
				max_link_slot=12,
				created_at=datetime.now(),
				group=ColorType.RED, hit_point=24, items=[]
			),
			SignType(
				id='2222222222',
				base_sign_types=[1],
				longitude=130.671892,
				latitude=33.654921,
				image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
				max_hit_point=100,
				max_item_slot=8,
				max_link_slot=12,
				created_at=datetime.now(),
				group=ColorType.RED, hit_point=24, items=[]
			),
			SignType(
				id='3333333333333333',
				base_sign_types=[1],
				longitude=130.671892,
				latitude=33.654921,
				image_path='https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/000/000/004/original/ed26601233e5b5cf.png',
				max_hit_point=100,
				max_item_slot=8,
				max_link_slot=12,
				created_at=datetime.now(),
				group=ColorType.RED, hit_point=24, items=[]
			),
		],
		segments=[
			Segment(
				id='444444444',
				sign_id='11111111111',
				other_sign_id='2222222222',
				created_at=datetime.now()
			),
			Segment(
				id='44',
				sign_id='2222222222',
				other_sign_id='3333333333333333',
				created_at=datetime.now()
			),
			Segment(
				id='4444',
				sign_id='11111111111',
				other_sign_id='3333333333333333',
				created_at=datetime.now()
			)
		],
		polygons=[
			PolygonType(
				id='88888888',
				group=ColorType.RED,
				surface=1.2456,
				sign_ids=['11111111111', '2222222222', '3333333333333333'],
				created_at=datetime.now()
			)
		]
	)
