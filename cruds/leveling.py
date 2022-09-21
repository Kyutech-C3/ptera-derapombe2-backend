from operator import le
from sqlalchemy.orm import Session
from db.models import Level
from schemas.leveling import Leveling

def get_leveling(db: Session, level: int) -> Leveling:
	leveling = db.query(Level).filter(Level.level == level).first()

	if leveling is None:
		raise Exception('leveling is not found')
	return Leveling(level=level, required_exp=leveling.required_exp)

