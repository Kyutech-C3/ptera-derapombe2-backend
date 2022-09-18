from fastapi.security import HTTPBearer
import firebase_admin
from firebase_admin import credentials, auth
from strawberry.types import Info

security = HTTPBearer()

cred = credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred)

def verify_token(info: Info):
	authorization = info.context['request'].headers.get('authorization')
	if authorization is None:
		raise Exception('token is not found')
	auth_list = authorization.split(' ')
	if len(auth_list) != 2 or auth_list[0] != 'Bearer':
		raise Exception('token format is invalid')

	try:
		user_info = auth.verify_id_token(auth_list[1])
	except Exception:
		raise Exception('verifying token is failed')
	user_id = user_info.get('user_id')
	if user_id is None:
		raise Exception('user_id is not found')
	return user_id
