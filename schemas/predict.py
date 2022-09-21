from typing import Optional
import strawberry

@strawberry.type()
class SuggestResult:
	score: float
	sign_type: int
	sign_name: str

@strawberry.type()
class PredictResult:
	status: bool
	scores: Optional[list[list[SuggestResult]]]
