from fastapi import APIRouter, Body

router = APIRouter()

@router.post('/register')
def register_user(username: str = Body(...), password: str = Body(...)):
    return {"status": "registered", "username": username}

@router.post('/login')
def login_user(username: str = Body(...), password: str = Body(...)):
    return {"access_token": "demo.jwt.token", "username": username}