import strawberry
import cruds.users as cu
from db.database import get_db
from schemas.users import AddUserInput, UserType
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

user_router = APIRouter()

def get_user(user_id: str) -> UserType:
	db = next(get_db())
	user = cu.get_user_by_id(db, user_id)
	return UserType.from_instance(user)

def get_users() -> list[UserType]:
	db = next(get_db())
	users = cu.get_users(db)
	return [UserType.from_instance(user) for user in users]

def add_user(user_input: AddUserInput) -> UserType:
	db = next(get_db())
	user = cu.create_user(db, **user_input.__dict__)
	return UserType.from_instance(user)

@strawberry.type
class UserQuery:
	user: UserType = strawberry.field(resolver=get_user)
	users: list[UserType] = strawberry.field(resolver=get_users)

@strawberry.type
class UserMutation:
	user_add: UserType = strawberry.field(resolver=add_user)

user_schema = strawberry.Schema(query=UserQuery, mutation=UserMutation)

user_router = GraphQLRouter(user_schema)
