from fastapi import APIRouter, Body
from core.nibbana import tracker

router = APIRouter()

@router.get('/progress')
def nibbana_progress(karma_total: int = 0, meditation_minutes: int = 0):
    prog = tracker.calc(karma_total, meditation_minutes)
    return {"progress": prog}