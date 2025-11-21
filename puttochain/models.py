# puttochain/models.py (เฉพาะส่วนที่เปลี่ยนแปลง)

class JournalEntry(Base):
    """
    ตาราง Journal Entries: บันทึกการกระทำดี/ชั่ว และผลการประเมิน
    """
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # --- เปลี่ยนจาก Column(Text) เป็น Column(String) สำหรับเก็บ CID ---
    ipfs_hash = Column(String, index=True, nullable=False) 
    
    is_good_deed = Column(Boolean, default=True)
    meditation_minutes = Column(Integer, default=0)
    
    # ผลลัพธ์จากการประเมิน
    karma_change = Column(Integer, default=0)
    ai_advice = Column(Text, nullable=True)
    
    # ... (Metadata และ Relationship เหมือนเดิม) ...
