from schemas.leveling import Leveling
from cruds import leveling as cl
from strawberry.types import Info
from db.database import get_db
from routers.utils import verify_token
from schemas.leveling import Leveling

def get_level(level: str, info: Info) -> Leveling:
	db = next(get_db())
	user_id = verify_token(info)

	leveling = cl.get_leveling(db, level)

	return leveling
