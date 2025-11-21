import React, { useState, useEffect } from 'react';

const KarmaDashboard = () => {
    const [karma, setKarma] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // จำลองการ Fetch ข้อมูลจาก FastAPI Backend API
        const fetchKarma = async () => {
            try {
                // แทนที่ URL ด้วย Backend API จริงของคุณ
                const response = await fetch('http://localhost:8000/karma/1'); 
                const data = await response.json();
                setKarma(data);
                setLoading(false);
            } catch (error) {
                console.error("Error fetching karma:", error);
                setLoading(false);
            }
        };

        fetchKarma();
    }, []);

    if (loading) {
        return <div className="text-center p-8 text-gray-500">Loading your Karma...</div>;
    }

    if (!karma) {
        return <div className="text-center p-8 text-red-500">Could not load Karma data.</div>;
    }

    return (
        <div className="max-w-md mx-auto bg-white shadow-xl rounded-2xl p-6 md:p-8 mt-10 border-t-4 border-indigo-500">
            <h2 className="text-3xl font-extrabold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">🕉️</span> Karma Dashboard
            </h2>
            <div className="space-y-4">
                <div className="bg-green-50 p-4 rounded-lg flex justify-between items-center">
                    <p className="text-lg font-medium text-gray-700">Karma Score:</p>
                    <p className="text-4xl font-bold text-green-600">{karma.score}</p>
                </div>
                
                <div className="bg-blue-50 p-4 rounded-lg flex justify-between items-center">
                    <p className="text-lg font-medium text-gray-700">Nibbana Level:</p>
                    <p className="text-xl font-semibold text-blue-600">{karma.level}</p>
                </div>
                
                <p className="text-sm text-center pt-4 text-gray-500">
                    "Every action you take shapes your Putthochain destiny."
                </p>
            </div>
        </div>
    );
};

export default KarmaDashboard;
