from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models import Color, Polygon
from schemas.polygons import PowerRatio

def calc_ratio(db: Session):
	red_surface = db.query(func.sum(Polygon.surface)).filter(Polygon.group == Color.RED).group_by(Polygon.group)
	green_surface = db.query(func.sum(Polygon.surface)).filter(Polygon.group == Color.GREEN).group_by(Polygon.group)

	PowerRatio(
		red=red_surface/(red_surface+green_surface),
		green=green_surface/(red_surface+green_surface)
	)
