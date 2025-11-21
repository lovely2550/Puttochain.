## main.py

# 1. คลาส JournalEntry (ที่จำเป็นสำหรับการคำนวณ)
class JournalEntry:
    def __init__(self, entry_type, value):
        # entry_type จะเป็น 'good' หรือ 'bad'
        self.entry_type = entry_type  
        self.value = value            

# 2. ฟังก์ชัน calculate_karma (ฟังก์ชันที่คุณต้องการทดสอบ)
def calculate_karma(entries):
    """คำนวณคะแนนกรรม (Karma Score) จากรายการทั้งหมด"""
    karma_score = 0
    for entry in entries:
        if entry.entry_type == 'good':
            karma_score += entry.value
        elif entry.entry_type == 'bad':
            karma_score -= entry.value
    return karma_score

if __name__ == '__main__':
    # ตัวอย่างการใช้งาน
    entry1 = JournalEntry('good', 10)
    entry2 = JournalEntry('bad', 5)
    entries_list = [entry1, entry2]
    score = calculate_karma(entries_list)
    print(f"Calculated Karma Score: {score}")
