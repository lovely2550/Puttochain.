import React, { useState, useEffect } from 'react';
import { fetchKarmaStatus } from '../services/putthochainApi';
import JournalForm from '../components/JournalForm';

const USER_ID = 1; // ต้องเปลี่ยนเป็น ID ผู้ใช้จริง

export default function Dashboard() {
    const [karmaData, setKarmaData] = useState(null);
    const [loading, setLoading] = useState(true);

    const loadKarmaStatus = async () => {
        setLoading(true);
        try {
            const data = await fetchKarmaStatus(USER_ID);
            setKarmaData(data);
        } catch (error) {
            console.error("Failed to load initial karma data:", error);
            setKarmaData(null);
        } finally {
            setLoading(false);
        }
    };
    
    // โหลดครั้งแรกเมื่อ Component Mount
    useEffect(() => {
        loadKarmaStatus();
    }, []);

    // Function ที่รับผลลัพธ์จาก JournalForm
    const handleJournalSuccess = (result) => {
        setKarmaData(result); // อัปเดต Karma Dashboard ทันที
        alert(`คำแนะนำจาก AI Somdej: ${result.ai_advice}`);
    };

    if (loading) {
        return <div className="text-center p-10">กำลังโหลดสถานะกรรม...</div>;
    }

    return (
        <div className="container mx-auto p-4 md:p-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* 📍 Col 1: Journal Submission */}
            <div className="lg:col-span-1">
                <JournalForm onSubmissionSuccess={handleJournalSuccess} />
            </div>

            {/* 📍 Col 2-3: Karma and AI Dashboard */}
            <div className="lg:col-span-2 space-y-8">
                {/* 1. สรุป Karma และ Nibbana */}
                <div className="bg-white p-6 shadow-xl rounded-2xl border-l-4 border-yellow-500">
                    <h2 className="text-3xl font-extrabold text-gray-900 mb-4">สรุปกรรมและนิพพาน</h2>
                    {karmaData ? (
                        <div className="grid grid-cols-2 gap-4">
                            <KarmaCard title="คะแนนกรรม (Karma Score)" value={karmaData.score} color="bg-green-100" />
                            <KarmaCard title="ระดับนิพพาน (Nibbana Level)" value={karmaData.level} color="bg-blue-100" />
                        </div>
                    ) : (
                        <p className="text-red-500">ไม่สามารถแสดงข้อมูล Karma ได้</p>
                    )}
                </div>

                {/* 2. AI Guidance */}
                {karmaData && (
                    <div className="bg-indigo-50 p-6 shadow-xl rounded-2xl border-l-4 border-indigo-500">
                        <h3 className="text-2xl font-bold text-indigo-700 flex items-center mb-3">
                            <span className="mr-2">🤖</span> AI Somdej Ong Pathom
                        </h3>
                        <p className="text-lg text-gray-700 italic">
                            "{karmaData.ai_advice}"
                        </p>
                        <p className="text-right text-sm mt-4 text-indigo-500">
                            - คำแนะนำสำหรับกรรมที่คุณได้บันทึกไว้
                        </p>
                    </div>
                )}
                
                {/* 3. Placeholder for DAO/Token */}
                <div className="text-center p-4 bg-gray-50 rounded-lg text-gray-600">
                    <p>🔗 **Blockchain Integration:** {karmaData?.score || 0} KMT Token ได้ถูก Mint/อัปเดตบน Polygon แล้ว</p>
                </div>
            </div>
        </div>
    );
}

// Helper Component (สำหรับแสดงผลสรุป)
const KarmaCard = ({ title, value, color }) => (
    <div className={`p-4 rounded-lg ${color}`}>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-3xl font-extrabold text-gray-800 mt-1">{value}</p>
    </div>
);
