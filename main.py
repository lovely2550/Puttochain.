# main.py (ส่วนที่เปลี่ยนแปลง)
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
# ... (imports เดิม)
from puttochain.database import engine, Base, get_db
from puttochain.models import User, JournalEntry
# --- NEW IMPORT ---
from puttochain.logging_config import setup_logging, logger 

# --- Call Setup Logging ---
setup_logging()
logger.info("Starting Putthochain API application.")

# ... (การกำหนดค่าและการสร้าง Instance ต่างๆ เหมือนเดิม) ...

@app.post("/journals/", response_model=KarmaScore, tags=["Journals & Karma"])
def create_journal_entry(
    entry_in: JournalEntryCreate, 
    db: Session = Depends(get_db) 
):
    
    # 1. ค้นหาผู้ใช้
    user = db.query(User).filter(User.wallet_address == entry_in.user_wallet_address).first()
    
    if not user:
        # บันทึกเมื่อมีการสร้าง User ใหม่
        logger.info(
            "New User created", 
            extra={'extra_data': {'wallet_address': entry_in.user_wallet_address, 'event': 'USER_CREATED'}}
        )
        user = User(wallet_address=entry_in.user_wallet_address)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # ... (ส่วนการคำนวณ Karma, AI Guidance, IPFS Upload) ...
    
    # 5. สร้าง Journal Entry ใหม่
    db_journal = JournalEntry(
        # ... (รายละเอียดการบันทึก) ...
    )
    db.add(db_journal)
    db.commit() 
    db.refresh(user)
    
    # บันทึกเมื่อ Journal ถูกบันทึกสำเร็จ
    logger.info(
        "Journal entry processed successfully", 
        extra={'extra_data': {
            'user_id': user.id, 
            'karma_change': karma_change,
            'ipfs_hash': ipfs_hash,
            'event': 'JOURNAL_PROCESSED'
        }}
    )

    # 6. Notification & Blockchain
    try:
        if karma_change > 0:
            blockchain_integrator.mint_karma_token(user.wallet_address, karma_change)
            logger.info(
                "KMT Mint initiated",
                extra={'extra_data': {'user_id': user.id, 'amount': karma_change, 'event': 'MINT_INITIATED'}}
            )
    except Exception as e:
        # บันทึก Critical Error หากการ Mint Token ล้มเหลว
        logger.error(
            "FATAL: KMT Mint failed", 
            exc_info=True,
            extra={'extra_data': {'user_id': user.id, 'error': str(e), 'event': 'MINT_FAILED'}}
        )
        # ควรมี logic การชดเชย (Compensation logic) ตรงนี้

    # ... (ส่วนการ Return Status) ...
    
    return KarmaScore(score=user.karma_score, level=level, ai_advice=advice)

# ... (Endpoint อื่นๆ เช่น get_user_karma_status ก็ควรเพิ่ม try/except และ logger.error เมื่อเกิดข้อผิดพลาด DB) ...
