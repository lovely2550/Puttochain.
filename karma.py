from fastapi import APIRouter, Body
from core.engine import karma_v2

router = APIRouter()

@router.post('/evaluate')
def evaluate_karma(action: str = Body(...)):
    score = karma_v2.score(action)
    return {"action": action, "karma_score": score}