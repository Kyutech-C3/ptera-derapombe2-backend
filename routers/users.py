import strawberry
import cruds.users as cu
from db.database import get_db
from schemas.users import AddUserInput, UserType
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
	if credentials.scheme != 'Bearer':
		raise HTTPException(status_code=403)
	# ここでtokenを確認し，firebaseからUserIdを受け取る
	# そのUserIdをcurrent_user_idとして渡す
	return {
		"current_user_id": credentials.credentials
	}

def get_user(user_id: str) -> UserType:
	db = next(get_db())
	user = cu.get_user_by_id(db, user_id)
	return UserType.from_instance(user)

def get_me(info: Info) -> UserType:
	db = next(get_db())
	me = cu.get_user_by_id(db, info.context['current_user_id'])
	return me

def add_user(user_input: AddUserInput) -> UserType:
	db = next(get_db())
	user = cu.create_user(db, **user_input.__dict__)
	return UserType.from_instance(user)

@strawberry.type
class UserQuery:
	user: UserType = strawberry.field(resolver=get_user)
	me: UserType = strawberry.field(resolver=get_me)

@strawberry.type
class UserMutation:
	user_add: UserType = strawberry.field(resolver=add_user)

user_schema = strawberry.Schema(query=UserQuery, mutation=UserMutation)

user_router = GraphQLRouter(user_schema, context_getter=auth)
