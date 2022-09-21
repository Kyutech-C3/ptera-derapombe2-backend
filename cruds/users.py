from db.models import User
from sqlalchemy.orm.session import Session
from schemas.users import ColorType

def get_user_by_id(db: Session, user_id: str) -> User:
	user = db.query(User).get(user_id)
	if user is None:
		raise Exception('user is not found')
	return user

def get_users(db: Session) -> list[User]:
	users = db.query(User).all()
	return users

def create_user(db: Session, user_id: str, name: str, group: ColorType, avatar_url: str) -> User:
	user = User(
		id=user_id,
		name=name,
		group=group,
		avatar_url=avatar_url
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user

def update_user(db: Session, user_id: str, name: str, avatar_url: str) -> User:
	user = get_user_by_id(db, user_id)
	user.name = name
	user.avatar_url = avatar_url
	db.commit()
	db.refresh(user)
	return user

