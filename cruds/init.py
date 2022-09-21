from db.database import get_db
from db.models import BaseSign, Item, ItemEffect
from sqlalchemy.orm import Session
import json

def init_item():
	db: Session = next(get_db())
	items = db.query(Item).first()
	if items is not None:
		return
	db.add(Item(
		name='耐久アップⅠ',
		level=1,
		effect=ItemEffect.ENDURANCE,
		value=10
	))
	db.add(Item(
		name='耐久アップⅡ',
		level=2,
		effect=ItemEffect.ENDURANCE,
		value=30
	))
	db.add(Item(
		name='耐久アップⅢ',
		level=3,
		effect=ItemEffect.ENDURANCE,
		value=50
	))
	db.add(Item(
		name='攻撃耐性Ⅰ',
		level=1,
		effect=ItemEffect.RESISTANCE,
		value=0.9
	))
	db.add(Item(
		name='攻撃耐性Ⅱ',
		level=2,
		effect=ItemEffect.RESISTANCE,
		value=0.8
	))
	db.add(Item(
		name='攻撃耐性Ⅲ',
		level=3,
		effect=ItemEffect.RESISTANCE,
		value=0.75
	))
	db.add(Item(
		name='回復Ⅰ',
		level=1,
		effect=ItemEffect.HEAL,
		value=10
	))
	db.add(Item(
		name='回復Ⅱ',
		level=2,
		effect=ItemEffect.HEAL,
		value=30
	))
	db.add(Item(
		name='回復Ⅲ',
		level=3,
		effect=ItemEffect.HEAL,
		value=50
	))
	db.add(Item(
		name='攻撃Ⅰ',
		level=1,
		effect=ItemEffect.ATTACK,
		value=10
	))
	db.add(Item(
		name='攻撃Ⅱ',
		level=2,
		effect=ItemEffect.ATTACK,
		value=30
	))
	db.add(Item(
		name='攻撃Ⅲ',
		level=3,
		effect=ItemEffect.ATTACK,
		value=50
	))
	db.commit()

def init_base_sign():
	json_open = open('./assets/SignTypeNameCorrespondenceTable.json', 'r')
	json_load = json.load(json_open)
	db: Session = next(get_db())
	base_sign = db.query(BaseSign).first()
	if base_sign is not None:
		return
	for i in range(200):
		bs = BaseSign(
			type=i,
			name=json_load[i]
		)
		db.add(bs)
	db.commit()
