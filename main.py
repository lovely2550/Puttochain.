# main.py (ส่วนที่เปลี่ยนแปลง)
from fastapi import FastAPI, HTTPException, Depends
# ...
from puttochain.database import engine, Base, get_db
from puttochain.models import User, JournalEntry # Import JournalEntry (updated)
from puttochain.ipfs_service import IPFSService # <--- NEW IMPORT

# ... (other imports) ...

# --- 1. การกำหนดค่าเริ่มต้นและ Instance ---
app = FastAPI(title="Putthochain API (IPFS Integration)")

ai_coach = AISomdejOngPathom()
notifier = FCMNotifier()
blockchain_integrator = BlockchainIntegrator()
ipfs_service = IPFSService() # <--- NEW INSTANCE

# Initialize Database - (ต้องรัน Base.metadata.create_all(bind=engine) อีกครั้ง)

# ... (Pydantic Schemas - JournalEntryCreate เหมือนเดิม) ...

@app.post("/journals/", response_model=KarmaScore, tags=["Journals & Karma"])
def create_journal_entry(
    entry_in: JournalEntryCreate, 
    db: Session = Depends(get_db)
):
    
    # 1. ค้นหาผู้ใช้ (Logic เดิม)
    user = db.query(User).filter(User.wallet_address == entry_in.user_wallet_address).first()
    # ... (logic for creating user if not exists) ...
    
    # 2. **IPFS:** อัปโหลด Journal Content และรับ Hash
    if not entry_in.content:
        raise HTTPException(status_code=400, detail="Journal content cannot be empty.")
        
    ipfs_hash = ipfs_service.upload_content(entry_in.content)
    
    # 3. คำนวณ Karma และอัปเดต User (Logic เดิม)
    karma_change = calculate_karma(entry_in) 
    user.karma_score += karma_change
    user.total_meditation_minutes += entry_in.meditation_minutes

    # 4. AI Guidance (ใช้ content เดิมก่อนจะทิ้งไป)
    advice = ai_coach.analyze_journal_and_advise(entry_in.content, entry_in.meditation_minutes)
    
    # 5. สร้าง Journal Entry ใหม่ (เก็บ Hash แทน Content)
    db_journal = JournalEntry(
        owner_id=user.id,
        ipfs_hash=ipfs_hash, # <--- STORE IPFS HASH
        is_good_deed=entry_in.is_good_deed,
        meditation_minutes=entry_in.meditation_minutes,
        karma_change=karma_change,
        ai_advice=advice
    )
    db.add(db_journal)
    db.commit() 
    db.refresh(user)

    # 6. Notification & Blockchain (Logic เดิม)
    # ...
    
    # 7. Return Status (Logic เดิม)
    # ...
    
    return KarmaScore(score=user.karma_score, level=level, ai_advice=advice)
