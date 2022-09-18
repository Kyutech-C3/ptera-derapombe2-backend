from db.models import User
from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from schemas.users import ColorType

def get_user_by_id(db: Session, user_id: str) -> User:
	user = db.query(User).get(user_id)
	if user is None:
		raise HTTPException(status_code=404, detail='user is not found')
	return user

def get_users(db: Session) -> list[User]:
	users = db.query(User).all()
	if users is None:
		raise HTTPException(status_code=404, detail='user is not found')
	return users

def create_user(db: Session, name: str, group: ColorType, avatar_number: int) -> User:
	user = User(
		name=name,
		group=group,
		avatar_number=avatar_number
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user
