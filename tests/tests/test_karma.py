import pytest
import sys
import os

# --- แก้ไข: เพิ่มพาธหลักเข้าไปในระบบเพื่อแก้ ModuleNotFoundError ---
# คำสั่งนี้จะทำให้ Python มองเห็นไฟล์ main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ----------------------------------------------------------------

# นำเข้าได้สำเร็จหลังจากการเพิ่มพาธ
from main import calculate_karma, JournalEntry 
from puttochain.ai_coach import AISomdejOngPathom
# ... (โค้ดที่เหลือเหมือนเดิม) ...
