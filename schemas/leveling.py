from typing import Optional
import strawberry

@strawberry.type()
class Leveling:
	level: int
	required_exp: int
