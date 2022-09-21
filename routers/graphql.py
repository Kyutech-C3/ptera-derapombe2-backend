import strawberry
from strawberry.fastapi import GraphQLRouter
from schemas.items import ItemType
from schemas.polygons import MapInfo, PowerRatio
from schemas.predict import PredictResult
from schemas.signs import ExhumeResult, Gallery, SignType, UpdateSignData
from schemas.users import UserType
from schemas.leveling import Leveling
from routers import (
	users as ru,
	polygons as rp,
	signs as rs,
	predict as pr,
	items as ri,
	leveling as rl
)

@strawberry.type
class Query:
	user: UserType = strawberry.field(resolver=ru.get_me)
	power_ratio: PowerRatio = strawberry.field(resolver=rp.get_power_ratio)
	sign: SignType = strawberry.field(resolver=rs.get_sign)
	items: list[ItemType] = strawberry.field(resolver=ri.get_my_items)
	galleries: list[Gallery] = strawberry.field(resolver=rs.get_my_galleries)
	# mock
	map_info: MapInfo = strawberry.field(resolver=rp.get_map_info)
	leveling: Leveling = strawberry.field(resolver=rl.get_level)

@strawberry.type
class Mutation:
	add_user: UserType = strawberry.field(resolver=ru.add_user)
	regist_sign: SignType = strawberry.field(resolver=rs.regist_sign)
	attach_item: list[ItemType] = strawberry.field(resolver=ri.attach_item)
	change_item: list[ItemType] = strawberry.field(resolver=ri.change_item)
	delete_item: list[ItemType] = strawberry.field(resolver=ri.delete_item)
	attack_sign: UpdateSignData = strawberry.field(resolver=ri.update_sign)
	heal_sign: UpdateSignData = strawberry.field(resolver=ri.update_sign)
	capture_sign: SignType = strawberry.field(resolver=rs.capture_sign)
	exhume_sign: ExhumeResult = strawberry.field(resolver=rs.exhume_sign)
	connect_signs: MapInfo = strawberry.field(resolver=rp.create_link)
	# mock
	update_user: UserType = strawberry.field(resolver=ru.update_user)
	predict_image: PredictResult = strawberry.field(resolver=pr.predict)

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_router = GraphQLRouter(schema)
