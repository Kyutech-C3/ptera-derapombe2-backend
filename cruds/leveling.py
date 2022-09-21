from operator import le
from sqlalchemy.orm import Session
from db.models import Level
from schemas.leveling import Leveling

def get_level_list(db: Session) -> list[int]:
	level_list = db.query(Level.required_exp).order_by(Level.level).all()

	return [level.required_exp for level in level_list]

