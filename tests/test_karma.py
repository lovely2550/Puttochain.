## tests/test_karma.py

# การนำเข้า (import) ที่ถูกแก้ไขเพื่อให้ Pytest พบโมดูล 'main'
from main import calculate_karma, JournalEntry


def test_calculate_karma_positive():
    """ทดสอบการคำนวณกรรมเมื่อมีแต่รายการดี"""
    entries = [
        JournalEntry('good', 5),
        JournalEntry('good', 10)
    ]
    expected_score = 15
    assert calculate_karma(entries) == expected_score


def test_calculate_karma_negative():
    """ทดสอบการคำนวณกรรมเมื่อมีแต่รายการแย่"""
    entries = [
        JournalEntry('bad', 5),
        JournalEntry('bad', 10)
    ]
    expected_score = -15
    assert calculate_karma(entries) == expected_score


def test_calculate_karma_mixed():
    """ทดสอบการคำนวณกรรมเมื่อมีรายการดีและแย่ปนกัน"""
    entries = [
        JournalEntry('good', 20),
        JournalEntry('bad', 5),
        JournalEntry('good', 2),
        JournalEntry('bad', 7)
    ]
    # ผลลัพธ์: 20 - 5 + 2 - 7 = 10
    expected_score = 10
    assert calculate_karma(entries) == expected_score


def test_calculate_karma_empty():
    """ทดสอบการคำนวณกรรมเมื่อไม่มีรายการ"""
    entries = []
    expected_score = 0
    assert calculate_karma(entries) == expected_score
