from cruds import leveling as cl
from strawberry.types import Info
from db.database import get_db
from routers.utils import verify_token
from schemas.leveling import Leveling

def get_requied_exp_point(info: Info) -> list[int]:
	db = next(get_db())
	verify_token(info)

	level_list = cl.get_level_list(db)

	return level_list
