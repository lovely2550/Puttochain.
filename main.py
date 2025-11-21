## main.py

# คลาส JournalEntry (ที่ถูก import ใน test_karma.py)
class JournalEntry:
    def __init__(self, entry_type, value):
        self.entry_type = entry_type
        self.value = value

# ฟังก์ชัน calculate_karma (ที่ถูก import ใน test_karma.py)
def calculate_karma(entries):
    """Calculates the karma score."""
    karma_score = 0
    for entry in entries:
        if entry.entry_type == 'good':
            karma_score += entry.value
        elif entry.entry_type == 'bad':
            karma_score -= entry.value
    return karma_score
