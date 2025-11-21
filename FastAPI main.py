from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from puttochain.ai_coach import AISomdejOngPathom # ต้องสร้างไฟล์นี้ตามตัวอย่างที่ให้ไป
from puttochain.notification import FCMNotifier # ต้องสร้างไฟล์นี้ตามตัวอย่างที่ให้ไป

# --- 1. การกำหนดค่าเริ่มต้นและ Instance ---
app = FastAPI(title="Putthochain API (Full Integration)")

# Instantiation ของโมดูลหลัก
ai_coach = AISomdejOngPathom()
notifier = FCMNotifier()

# --- 2. Pydantic Schemas ---
class JournalEntry(BaseModel):
    user_id: int
    user_fcm_token: str # สำหรับส่ง Notification
    content: str
    is_good_deed: bool 
    meditation_minutes: int = 0

class KarmaScore(BaseModel):
    score: int
    level: str
    ai_advice: str

# --- 3. MOCKUP Data Store ---
karma_db: Dict[int, int] = {1: 100, 2: 50} 

# --- 4. CORE Module: Karma Engine ---
def calculate_karma(entry: JournalEntry) -> int:
    """ ประเมินคะแนนกรรมดี/ชั่วตามกิจกรรม """
    karma_change = 0
    
    if entry.is_good_deed:
        karma_change += 10
    else:
        # การกระทำที่ไม่ดี หรือต้องการพิจารณา
        karma_change -= 5

    # ให้รางวัลสำหรับการทำสมาธิ (Nibbana Tracker)
    karma_change += entry.meditation_minutes // 5
    
    # ... Logic สำหรับ Blockchain Monitor, AI Ethics Engine ...
    
    return karma_change

# --- 5. API Endpoints ---
@app.post("/journals/", response_model=KarmaScore, tags=["Journals & Karma"])
def create_journal_entry(entry: JournalEntry):
    user_id = entry.user_id
    
    # 1. คำนวณ Karma
    karma_change = calculate_karma(entry)
    new_karma_score = karma_db.get(user_id, 0) + karma_change
    karma_db[user_id] = new_karma_score
    
    # 2. AI Guidance (Somdej Ong Pathom)
    advice = ai_coach.analyze_journal_and_advise(entry.content, entry.meditation_minutes)
    
    # 3. Notification (FCM)
    notifier.send_karma_update(entry.user_fcm_token, new_karma_score, karma_change)
    notifier.send_ai_guidance(entry.user_fcm_token, advice)
    
    # 4. Blockchain Integration (Mockup)
    # สมมติว่านี่คือจุดที่จะเรียก Smart Contract mint_karma_token(user_id, karma_change)
    print(f"[Blockchain MOCK] Minting {karma_change} KMT tokens for User {user_id}")
    
    level = "Bodhisattva" if new_karma_score > 500 else "Practitioner" if new_karma_score > 100 else "Beginner"
    
    return KarmaScore(score=new_karma_score, level=level, ai_advice=advice)

@app.get("/karma/{user_id}", response_model=KarmaScore, tags=["Karma"])
def get_user_karma_status(user_id: int):
    score = karma_db.get(user_id)
    if score is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # จำลองการให้คำแนะนำสั้นๆ เมื่อเรียกดูสถานะ
    advice = "สติเป็นเครื่องนำทาง จงพิจารณา"
    level = "Bodhisattva" if score > 500 else "Practitioner" if score > 100 else "Beginner"

    return KarmaScore(score=score, level=level, ai_advice=advice)
