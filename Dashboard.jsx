// src/pages/Dashboard.jsx (ส่วนที่เปลี่ยนแปลง)
import TokenStatusCard from '../components/TokenStatusCard'; // นำเข้า
import DaoVotingCard from '../components/DaoVotingCard'; // นำเข้า
// ... (โค้ดเดิม)

export default function Dashboard() {
    // ... (โค้ดเดิม)

    return (
        <div className="container mx-auto p-4 md:p-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* 📍 Col 1: Journal Submission */}
            <div className="lg:col-span-1 space-y-8">
                <JournalForm onSubmissionSuccess={handleJournalSuccess} />
                <TokenStatusCard /> {/* <--- เพิ่ม Token Status */}
            </div>

            {/* 📍 Col 2-3: Karma, AI, and DAO Dashboard */}
            <div className="lg:col-span-2 space-y-8">
                {/* 1. สรุป Karma และ Nibbana */}
                <div className="bg-white p-6 shadow-xl rounded-2xl border-l-4 border-yellow-500">
                   {/* ... (Karma/Nibbana Cards) ... */}
                </div>

                {/* 2. AI Guidance */}
                {/* ... (AI Somdej Ong Pathom Card) ... */}
                
                {/* 3. DAO Voting Section */}
                <DaoVotingCard /> {/* <--- เพิ่ม DAO Voting */}
                
            </div>
        </div>
    );
}
