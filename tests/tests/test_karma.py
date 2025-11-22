import pytest
import sys
import os

# --- เริ่มการแก้ไข: เพิ่มพาธหลักของโปรเจกต์เข้าไปในระบบ ---
# บรรทัดนี้จะทำให้ Python สามารถค้นหาไฟล์ main.py ได้
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --------------------------------------------------------

# บรรทัดนี้จะทำงานได้สำเร็จหลังจากการแก้ไขด้านบน
from main import calculate_karma, JournalEntry 
from puttochain.ai_coach import AISomdejOngPathom

# ... (โค้ดที่เหลือเหมือนเดิม) ...
