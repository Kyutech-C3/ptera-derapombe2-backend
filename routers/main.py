import strawberry
from strawberry.fastapi import GraphQLRouter
from schemas.users import UserType
import users as ru

@strawberry.type
class Query:
	user: UserType = strawberry.field(resolver=ru.get_user)
	me: UserType = strawberry.field(resolver=ru.get_me)

@strawberry.type
class Mutation:
	add_user: UserType = strawberry.field(resolver=ru.add_user)

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_router = GraphQLRouter(schema)
