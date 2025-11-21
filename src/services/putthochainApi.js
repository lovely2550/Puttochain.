// กำหนด Base URL ของ Backend (เปลี่ยนเป็น URL Deployment จริง)
const API_BASE_URL = 'http://localhost:8000'; 

/**
 * บันทึก Journal และรับ Karma Status กลับมา
 * @param {object} entry - ข้อมูล Journal ที่ผู้ใช้ป้อน
 */
export async function submitJournalEntry(entry) {
    try {
        const response = await fetch(`${API_BASE_URL}/journals/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(entry),
        });

        if (!response.ok) {
            // โยน Error หาก API ตอบกลับด้วยสถานะไม่สำเร็จ (4xx, 5xx)
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to submit journal.');
        }

        return await response.json(); // คืนค่า KarmaScore และ AI Advice
    } catch (error) {
        console.error("API Error during journal submission:", error);
        throw error;
    }
}

/**
 * ดึงข้อมูล Karma และ Nibbana Progress
 * @param {number} userId - ID ของผู้ใช้ปัจจุบัน
 */
export async function fetchKarmaStatus(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/karma/${userId}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch karma status.');
        }

        return await response.json(); // คืนค่า KarmaScore
    } catch (error) {
        console.error("API Error during karma status fetch:", error);
        throw error;
    }
}
