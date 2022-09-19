import strawberry
from strawberry.fastapi import GraphQLRouter
from schemas.users import UserType
from .users import get_user, get_me, add_user

@strawberry.type
class Query:
	user: UserType = strawberry.field(resolver=get_user)
	me: UserType = strawberry.field(resolver=get_me)

@strawberry.type
class Mutation:
	user_add: UserType = strawberry.field(resolver=add_user)

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_router = GraphQLRouter(schema)
