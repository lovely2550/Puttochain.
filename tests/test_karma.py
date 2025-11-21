# ต้องนำเข้าฟังก์ชันจากไฟล์โค้ดหลักที่คุณสร้างไว้
from main import calculate_karma, JournalEntry # สมมติว่า main.py มีการนำเข้า JournalEntry
from puttochain.ai_coach import AISomdejOngPathom
import pytest

# --- เตรียมข้อมูล Mockup สำหรับการทดสอบ ---
# (ใช้ MOCKUP data ที่ใกล้เคียงกับการเรียกใช้จริง)
user_data_mock = {
    "user_id": 99,
    "user_fcm_token": "test-token",
    "user_wallet_address": "0xTestWalletAddress"
}

# --- 1. ทดสอบ Karma Engine Logic ---
def test_karma_good_deed_increase():
    """ทดสอบว่า Karma เพิ่มขึ้นเมื่อเป็นการกระทำดี"""
    entry_data = JournalEntry(
        **user_data_mock, 
        content="ช่วยเพื่อนร่วมงาน", 
        is_good_deed=True, 
        meditation_minutes=0
    )
    change = calculate_karma(entry_data)
    # คาดหวังการเพิ่มขึ้นตาม logic ใน calculate_karma (10 คะแนน)
    assert change == 10

def test_karma_neutral_deed_decrease():
    """ทดสอบว่า Karma ลดลงเมื่อไม่ใช่การกระทำดี (กลางๆ/อาจต้องระวัง)"""
    entry_data = JournalEntry(
        **user_data_mock, 
        content="บ่นเรื่องงานเล็กน้อย", 
        is_good_deed=False, 
        meditation_minutes=0
    )
    change = calculate_karma(entry_data)
    # คาดหวังการลดลงตาม logic ใน calculate_karma (-5 คะแนน)
    assert change == -5

def test_karma_meditation_bonus():
    """ทดสอบโบนัส Karma จากการทำสมาธิ (Nibbana Tracker)"""
    # 25 นาที (คาดหวัง +5 คะแนน จาก 25 // 5)
    entry_data = JournalEntry(
        **user_data_mock, 
        content="ทำสมาธิอย่างสงบ", 
        is_good_deed=True, 
        meditation_minutes=25
    )
    # Karma เปลี่ยนแปลง = Good Deed (10) + Meditation (5) = 15
    change = calculate_karma(entry_data)
    assert change == 15

# --- 2. ทดสอบ AI Somdej Ong Pathom Logic ---
@pytest.fixture
def ai_coach_instance():
    """Fixture สำหรับสร้าง Instance ของ AI Coach"""
    return AISomdejOngPathom()

def test_ai_advice_short_journal(ai_coach_instance):
    """ทดสอบคำแนะนำสำหรับ Journal สั้นๆ"""
    content = "ทำดี."
    advice = ai_coach_instance.analyze_journal_and_advise(content, 5)
    # ควรมีคำแนะนำเกี่ยวกับ 'short' journal
    assert "ลองเจาะลึกอารมณ์ให้มากขึ้น" in advice

def test_ai_advice_long_journal(ai_coach_instance):
    """ทดสอบคำแนะนำสำหรับ Journal ยาวๆ"""
    content = "A" * 60 # เกิน 50 คำ (word count > 50)
    advice = ai_coach_instance.analyze_journal_and_advise(content, 0)
    # ควรมีคำแนะนำเกี่ยวกับ 'long' journal (วิริยะนำทาง)
    assert "วิริยะนำทาง" in advice
    
def test_ai_advice_meditation_focus(ai_coach_instance):
    """ทดสอบคำแนะนำที่เน้นการทำสมาธิ (15 นาที+)"""
    content = "..."
    advice = ai_coach_instance.analyze_journal_and_advise(content, 20)
    # ควรมีคำแนะนำเกี่ยวกับ 'meditate'
    assert "จิตที่สงบคือปัญญา" in advice
