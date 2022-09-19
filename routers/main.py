import strawberry
from strawberry.fastapi import GraphQLRouter
from schemas.items import ItemType
from schemas.polygons import PowerRatio
from schemas.predict import PredictResult
from schemas.signs import AttackResult, ExhumeResult, Gallery, SignInfo, SignStatusType, SignType
from schemas.users import UserType
from routers import (
	users as ru,
	polygons as rp,
	signs as rs,
	items as ri
)

@strawberry.type
class Query:
	power_ratio: PowerRatio = strawberry.field(resolver=rp.get_power_ratio)
	user: UserType = strawberry.field(resolver=ru.get_user)
	me: UserType = strawberry.field(resolver=ru.get_me)
	sign_info: SignInfo = strawberry.field(resolver=rs.get_sign_info)
	sign_status: SignStatusType = strawberry.field(resolver=rs.get_sign_status)
	my_items: list[ItemType] = strawberry.field(resolver=ri.get_my_items)
	my_galleries: list[Gallery] = strawberry.field(resolver=rs.get_my_galleries)

@strawberry.type
class Mutation:
	add_user: UserType = strawberry.field(resolver=ru.add_user)
	update_user: UserType = strawberry.field(resolver=ru.update_user)
	add_item: list[ItemType] = strawberry.field(resolver=ri.add_item)
	change_item: list[ItemType] = strawberry.field(resolver=ri.change_item)
	delete_item: list[ItemType] = strawberry.field(resolver=ri.delete_item)
	capture_sign: list[SignType] = strawberry.field(resolver=rs.capture_sign)
	exhume_sign: list[ExhumeResult] = strawberry.field(resolver=rs.exhume_sign)
	attack_sign: AttackResult = strawberry.field(resolver=rs.attack_sign)
	predict_image: PredictResult = strawberry.field(resolver=rs.predict_image)

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_router = GraphQLRouter(schema)
