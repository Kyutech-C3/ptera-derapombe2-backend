import strawberry
from strawberry.fastapi import GraphQLRouter
from schemas.items import ItemType
from schemas.polygons import MapInfo, PowerRatio
from schemas.predict import PredictResult
from schemas.signs import AttackResult, ExhumeResult, Gallery, SignType
from schemas.users import UserType
from routers import (
	users as ru,
	polygons as rp,
	signs as rs,
	predict as pr,
	items as ri
)

@strawberry.type
class Query:
	user: UserType = strawberry.field(resolver=ru.get_me)
	# mock
	power_ratio: PowerRatio = strawberry.field(resolver=rp.get_power_ratio)
	sign: SignType = strawberry.field(resolver=rs.get_sign)
	items: list[ItemType] = strawberry.field(resolver=ri.get_my_items)
	galleries: list[Gallery] = strawberry.field(resolver=rs.get_my_galleries)
	map_info: MapInfo = strawberry.field(resolver=rp.get_map_info)

@strawberry.type
class Mutation:
	add_user: UserType = strawberry.field(resolver=ru.add_user)
	regist_sign: SignType = strawberry.field(resolver=rs.regist_sign)
	# mock
	update_user: UserType = strawberry.field(resolver=ru.update_user)
	add_item: list[ItemType] = strawberry.field(resolver=ri.add_item)
	change_item: list[ItemType] = strawberry.field(resolver=ri.change_item)
	delete_item: list[ItemType] = strawberry.field(resolver=ri.delete_item)
	capture_sign: SignType = strawberry.field(resolver=rs.capture_sign)
	exhume_sign: list[ExhumeResult] = strawberry.field(resolver=rs.exhume_sign)
	attack_sign: AttackResult = strawberry.field(resolver=rs.attack_sign)
	predict_image: PredictResult = strawberry.field(resolver=pr.predict)

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_router = GraphQLRouter(schema)
