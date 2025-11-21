from fastapi import APIRouter, Body
from core.somdej_ai import somdej_voice

router = APIRouter()

@router.post('/advice')
def somdej_advice(user_input: str = Body(...)):
    reply = somdej_voice(user_input)
    return {"advice": reply}