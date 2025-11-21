import pytest
import sys
import os

# --- เพิ่ม 3 บรรทัดนี้เพื่อแก้ไขปัญหา ModuleNotFoundError ---
# คำสั่งนี้จะเพิ่มพาธหลักของโปรเจกต์ (โฟลเดอร์ Puttochain) เข้าไปใน Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -----------------------------------------------------------

# บรรทัดนี้จะทำงานได้สำเร็จหลังจากการแก้ไขด้านบน
from main import calculate_karma, JournalEntry 
from puttochain.ai_coach import AISomdejOngPathom

# ... (โค้ดที่เหลือเหมือนเดิม) ...
