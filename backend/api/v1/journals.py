from fastapi import APIRouter, Body

router = APIRouter()
JOURNALS = []

@router.post('/')
def add_journal(uid: int = Body(...), text: str = Body(...)):
    data = {"id": len(JOURNALS) + 1, "uid": uid, "text": text}
    JOURNALS.append(data)
    return data

@router.get('/')
def list_journals():
    return JOURNALS