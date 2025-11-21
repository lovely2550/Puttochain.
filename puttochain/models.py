from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    """
    ตาราง Users: เก็บข้อมูลผู้ใช้, Karma Score, และ Nibbana Progress
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, unique=True, index=True, nullable=False) # ใช้เป็น ID หลักในการระบุตัวตน
    fcm_token = Column(String, nullable=True) # สำหรับ Notification
    
    # Karma System
    karma_score = Column(Integer, default=0)
    
    # Nibbana Tracker (Simplified)
    total_meditation_minutes = Column(Integer, default=0)
    
    # Relationship
    journals = relationship("JournalEntry", back_populates="owner")
    
    
class JournalEntry(Base):
    """
    ตาราง Journal Entries: บันทึกการกระทำดี/ชั่ว และผลการประเมิน
    """
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id")) # เชื่อมโยงกับผู้ใช้
    
    content = Column(Text, nullable=False)
    is_good_deed = Column(Boolean, default=True)
    meditation_minutes = Column(Integer, default=0)
    
    # ผลลัพธ์จากการประเมิน
    karma_change = Column(Integer, default=0)
    ai_advice = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    owner = relationship("User", back_populates="journals")
