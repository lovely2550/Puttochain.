import pytest
import sys
import os

# แก้ไขปัญหา ModuleNotFoundError: เพิ่มพาธหลักเข้าไปในระบบ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ตอนนี้นำเข้าไฟล์ main.py ได้
from main import calculate_karma, JournalEntry 
from puttochain.ai_coach import AISomdejOngPathom

# --- ข้อมูล Mockup สำหรับการทดสอบ ---
user_data_mock = {
    "user_id": 99,
    "user_fcm_token": "test-token",
    "user_wallet_address": "0xTestWalletAddress"
}

# --- 1. ทดสอบ Karma Engine Logic ---
def test_karma_good_deed_increase():
    # ... (โค้ดทดสอบเหมือนเดิม) ...
    entry_data = JournalEntry(
        **user_data_mock, 
        content="ช่วยเพื่อนร่วมงาน", 
        is_good_deed=True, 
        meditation_minutes=0
    )
    change = calculate_karma(entry_data)
    assert change == 10

# ... (โค้ดทดสอบอื่น ๆ ต่อไป) ...
