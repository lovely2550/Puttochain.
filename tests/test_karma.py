import pytest
import sys
import os

# --- FINAL FIX: การจัดการพาธเพื่อให้ Python ค้นพบ main.py ในโฟลเดอร์หลัก ---
# (สำคัญ: ทำซ้ำโค้ดนี้ใน tests/test_api_endpoints.py และ tests/conftest.py ด้วย)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -------------------------------------------------------------------------

# ตอนนี้สามารถนำเข้าได้โดยไม่มีข้อผิดพลาด
from main import calculate_karma, JournalEntry 
from puttochain.ai_coach import AISomdejOngPathom

# ... (โค้ดทดสอบที่เหลือ) ...
