from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models import Color, Polygon
from schemas.polygons import PowerRatio

def calc_power_ratio(db: Session):
	red_surface = db.query(func.sum(Polygon.surface)).filter(Polygon.group == Color.RED).group_by(Polygon.group).first()
	if red_surface is None:
		red_surface = 0
	green_surface = db.query(func.sum(Polygon.surface)).filter(Polygon.group == Color.GREEN).group_by(Polygon.group).first()
	if green_surface is None:
		green_surface = 0

	return PowerRatio(
		red=red_surface/(red_surface+green_surface) if (red_surface+green_surface) > 0 else 0.5,
		green=green_surface/(red_surface+green_surface) if (red_surface+green_surface) > 0 else 0.5
	)
