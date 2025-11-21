from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="Putthochain Backend API")

# --- Pydantic Schemas ---
class JournalEntry(BaseModel):
    user_id: int
    content: str
    is_good_deed: bool # ใช้ในการประเมิน Karma
    meditation_minutes: int = 0

class KarmaScore(BaseModel):
    score: int
    level: str

# --- MOCKUP Data Store ---
journals_db: Dict[int, JournalEntry] = {}
karma_db: Dict[int, int] = {1: 100} # User 1 เริ่มต้นที่ 100 Karma

# --- CORE Module: Karma Engine Mockup ---
def calculate_karma(entry: JournalEntry) -> int:
    """
    Simulates the Karma Engine (ประเมินคะแนนกรรม).
    """
    karma_change = 0
    
    if entry.is_good_deed:
        karma_change += 5
    else:
        # สมมติว่าการบันทึกที่ไม่ใช่กรรมดีอาจเป็นกลางหรือต้องระวัง
        karma_change -= 2

    # ให้รางวัลสำหรับการทำสมาธิ (Nibbana Tracker)
    karma_change += entry.meditation_minutes // 10
    
    return karma_change

# --- API Endpoints ---
@app.get("/", tags=["Status"])
def read_root():
    return {"message": "Putthochain API is running (FastAPI)"}

@app.post("/journals/", response_model=JournalEntry, tags=["Journals"])
def create_journal_entry(entry: JournalEntry):
    # บันทึก Journal
    journals_db[len(journals_db) + 1] = entry
    
    # คำนวณ Karma
    karma_change = calculate_karma(entry)
    user_id = entry.user_id
    
    # อัปเดต Karma
    karma_db[user_id] = karma_db.get(user_id, 0) + karma_change
    
    return entry

@app.get("/karma/{user_id}", response_model=KarmaScore, tags=["Karma"])
def get_karma_score(user_id: int):
    score = karma_db.get(user_id)
    if score is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    level = "Bodhisattva" if score > 500 else "Practitioner" if score > 100 else "Beginner"
    
    return KarmaScore(score=score, level=level)

# รันด้วย uvicorn main:app --reload
