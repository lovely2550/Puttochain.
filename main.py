## main.py

# 1. คลาส JournalEntry
class JournalEntry:
    def __init__(self, entry_type, value):
        self.entry_type = entry_type
        self.value = value

# 2. ฟังก์ชัน calculate_karma
def calculate_karma(entries):
    """คำนวณคะแนนกรรม (Karma Score) จากรายการทั้งหมด"""
    karma_score = 0
    for entry in entries:
        if entry.entry_type == 'good':
            karma_score += entry.value
        elif entry.entry_type == 'bad':
            karma_score -= entry.value
    return karma_score
