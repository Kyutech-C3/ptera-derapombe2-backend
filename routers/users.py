import strawberry
import cruds.users as cu
from db.database import get_db
from schemas.users import AddUserInput, UserType
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
	if credentials.scheme != 'Bearer':
		raise HTTPException(status_code=403)
	try:
		user_info = auth.verify_id_token(credentials.credentials)
	except Exception:
		raise HTTPException(
			status_code=401
		)

	user_id = user_info.get('user_id')
	if user_id is None:
		raise HTTPException(
			status_code=400
		)

	return {
		"current_user_id": user_id
	}

def get_user(user_id: str) -> UserType:
	db = next(get_db())
	user = cu.get_user_by_id(db, user_id)
	return UserType.from_instance(user)

def get_me(info: Info) -> UserType:
	db = next(get_db())
	user_id = info.context['current_user_id']
	me = cu.get_user_by_id(db, user_id)
	return me

def add_user(user_input: AddUserInput, info: Info) -> UserType:
	db = next(get_db())
	user_id = info.context['current_user_id']
	user = cu.create_user(db, user_id, **user_input.__dict__)
	return UserType.from_instance(user)

@strawberry.type
class UserQuery:
	user: UserType = strawberry.field(resolver=get_user)
	me: UserType = strawberry.field(resolver=get_me)

@strawberry.type
class UserMutation:
	user_add: UserType = strawberry.field(resolver=add_user)

user_schema = strawberry.Schema(query=UserQuery, mutation=UserMutation)

user_router = GraphQLRouter(user_schema, context_getter=verify_token)
