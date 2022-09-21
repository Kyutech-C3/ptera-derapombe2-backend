from datetime import datetime
from strawberry.file_uploads import Upload
from schemas.general import ColorType, ItemEffectType
from schemas.items import ItemType
from schemas.predict import PredictResult, SuggestResult
from schemas.signs import ExhumeResult, Gallery, RegistSignInput, SignInfo, SignType
from cruds import signs as cs
from strawberry.types import Info
from db.database import get_db
from routers.utils import verify_token

def regist_sign(regist_sign_input: RegistSignInput, info: Info) -> SignType:
	db = next(get_db())
	user_id = verify_token(info)
	new_sign = cs.regist_sign(
		db, user_id, regist_sign_input.base_sign_types,
		regist_sign_input.coordinate.longitude,
		regist_sign_input.coordinate.latitude,
		regist_sign_input.image_path
	)
	return new_sign

def capture_sign(sign_id: str, info: Info) -> SignType:
	db = next(get_db())
	user_id = verify_token(info)
	new_sign = cs.capture_sign(db, sign_id, user_id)
	return new_sign

def exhume_sign(sign_id: str, info: Info) -> ExhumeResult:
	db = next(get_db())
	user_id = verify_token(info)
	result = cs.exhume_sign(db, sign_id, user_id)
	return result

def get_sign(sign_id: str, info: Info) -> SignType:
	db = next(get_db())
	verify_token(info)
	sign = cs.get_sign_by_id(db, sign_id)
	return sign

def get_my_galleries(info: Info) -> list[Gallery]:
	db = next(get_db())
	user_id = verify_token(info)
	my_galleries = cs.get_user_galleries(db, user_id)
	return my_galleries
