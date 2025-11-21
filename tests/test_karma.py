## tests/test_karma.py

# การนำเข้าที่ทำให้เกิดปัญหาในภาพ (ต้องมั่นใจว่า main.py ถูกพบ)
# บรรทัดนี้คือบรรทัดที่ 30 ใน Traceback ของคุณ
from main import calculate_karma, JournalEntry


def test_karma_calculation_is_correct():
    """Test mixed entries to ensure calculate_karma works."""
    entries = [
        JournalEntry('good', 10),
        JournalEntry('bad', 3),
        JournalEntry('good', 5)
    ]
    # 10 - 3 + 5 = 12
    expected_score = 12
    assert calculate_karma(entries) == expected_score

def test_empty_list_returns_zero():
    """Test that an empty list returns 0."""
    assert calculate_karma([]) == 0
