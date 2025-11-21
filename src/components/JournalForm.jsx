import React, { useState } from 'react';
import { submitJournalEntry } from '../services/putthochainApi';

const USER_MOCKUP = {
    user_id: 1, // ต้องเปลี่ยนเป็น ID ผู้ใช้จริง
    user_fcm_token: "mock-fcm-token-123", // Token สำหรับแจ้งเตือน
    user_wallet_address: "0x123...456" // Wallet Address สำหรับ Mint KMT
};

export default function JournalForm({ onSubmissionSuccess }) {
    const [content, setContent] = useState('');
    const [isGoodDeed, setIsGoodDeed] = useState(true);
    const [meditationMinutes, setMeditationMinutes] = useState(0);
    const [status, setStatus] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('Submitting...');

        const entryData = {
            ...USER_MOCKUP,
            content,
            is_good_deed: isGoodDeed,
            meditation_minutes: parseInt(meditationMinutes),
        };

        try {
            const result = await submitJournalEntry(entryData);
            setStatus('Submission successful! Check dashboard.');
            setContent('');
            setMeditationMinutes(0);
            
            // ส่งผลลัพธ์ไปยัง Dashboard Component
            onSubmissionSuccess(result); 

        } catch (error) {
            setStatus(`Error: ${error.message}`);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="p-6 bg-white shadow-xl rounded-lg space-y-4">
            <h3 className="text-2xl font-bold text-gray-800">บันทึกกรรม (Journal)</h3>
            
            <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="วันนี้คุณทำอะไร? (สะท้อนการกระทำดี/ชั่ว)"
                required
                rows="4"
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            />

            <div className="flex items-center space-x-4">
                <label className="flex items-center text-gray-700">
                    <input
                        type="checkbox"
                        checked={isGoodDeed}
                        onChange={(e) => setIsGoodDeed(e.target.checked)}
                        className="h-5 w-5 text-indigo-600 rounded"
                    />
                    <span className="ml-2 font-medium">เป็นการกระทำดี (Good Deed)</span>
                </label>
            </div>

            <label className="block text-gray-700">
                เวลาทำสมาธิ (นาที):
                <input
                    type="number"
                    value={meditationMinutes}
                    onChange={(e) => setMeditationMinutes(e.target.value)}
                    min="0"
                    className="mt-1 w-full p-2 border border-gray-300 rounded-md"
                />
            </label>
            
            <button
                type="submit"
                className="w-full bg-indigo-600 text-white py-3 rounded-md font-semibold hover:bg-indigo-700 transition duration-150"
            >
                บันทึกและคำนวณ Karma
            </button>
            
            {status && <p className={`text-center font-medium ${status.startsWith('Error') ? 'text-red-500' : 'text-green-600'}`}>{status}</p>}
        </form>
    );
}
