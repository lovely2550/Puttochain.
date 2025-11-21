# main.py (ส่วนที่เปลี่ยนแปลง)
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session # New dependency
# Import Database and Models
from puttochain.database import engine, Base, get_db
from puttochain.models import User, JournalEntry
# ... (other imports: ai_coach, notifier, blockchain_integrator, calculate_karma)

# Initialize Database - สร้างตารางทั้งหมดถ้ายังไม่มี
Base.metadata.create_all(bind=engine)

# ... (Pydantic Schemas - JournalEntryCreate ถูกปรับให้รับ wallet_address แทน ID) ...

@app.post("/journals/", response_model=KarmaScore, tags=["Journals & Karma"])
def create_journal_entry(
    entry_in: JournalEntryCreate, 
    db: Session = Depends(get_db) # <--- ใช้ Dependency Injection
):
    
    # 1. ค้นหาผู้ใช้ด้วย Wallet Address, ถ้าไม่เจอให้สร้างใหม่
    user = db.query(User).filter(User.wallet_address == entry_in.user_wallet_address).first()
    
    if not user:
        user = User(wallet_address=entry_in.user_wallet_address)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 2. คำนวณ Karma และอัปเดต User
    karma_change = calculate_karma(entry_in) 
    user.karma_score += karma_change
    user.total_meditation_minutes += entry_in.meditation_minutes # Nibbana Tracker

    # 3. AI Guidance และสร้าง Journal Entry ใหม่
    advice = ai_coach.analyze_journal_and_advise(entry_in.content, entry_in.meditation_minutes)
    db_journal = JournalEntry(
        owner_id=user.id,
        content=entry_in.content,
        is_good_deed=entry_in.is_good_deed,
        meditation_minutes=entry_in.meditation_minutes,
        karma_change=karma_change,
        ai_advice=advice
    )
    db.add(db_journal)
    db.commit() # บันทึก Journal และ User Changes พร้อมกัน
    db.refresh(user) 

    # 4. Notification & Blockchain (ใช้ข้อมูลจาก User object)
    if user.fcm_token:
        notifier.send_karma_update(user.fcm_token, user.karma_score, karma_change)
    if karma_change > 0:
        blockchain_integrator.mint_karma_token(user.wallet_address, karma_change)
    
    # 5. Return Status
    level = "Bodhisattva" if user.karma_score > 500 else "Practitioner" if user.karma_score > 100 else "Beginner"
    return KarmaScore(score=user.karma_score, level=level, ai_advice=advice)


@app.get("/karma/{wallet_address}", response_model=KarmaScore, tags=["Karma"])
def get_user_karma_status(wallet_address: str, db: Session = Depends(get_db)):
    """ดึงข้อมูลจาก DB ด้วย wallet_address"""
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # ... (ส่วนการคำนวณ Level และ Advice เหมือนเดิม) ...
