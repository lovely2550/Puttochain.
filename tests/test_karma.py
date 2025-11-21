## tests/test_karma.py

# การนำเข้าที่ทำให้เกิดปัญหาในภาพ: ต้องมั่นใจว่า main.py ถูกพบ
from main import calculate_karma, JournalEntry


def test_calculate_karma_mixed():
    """ทดสอบการคำนวณกรรม (ตัวอย่างการทดสอบ)"""
    entries = [
        JournalEntry('good', 20),
        JournalEntry('bad', 5),
    ]
    # 20 - 5 = 15
    expected_score = 15
    assert calculate_karma(entries) == expected_score

# (คุณสามารถเพิ่มการทดสอบอื่น ๆ ได้ตามต้องการ)
