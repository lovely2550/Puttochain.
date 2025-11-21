import React, { useState, useEffect } from 'react';

// Mockup Data สำหรับข้อเสนอเชิงจริยธรรม
const mockProposals = [
    { id: 1, description: "ควรลดคะแนนกรรมสำหรับการโพสต์ข้อความเชิงลบในวันพระหรือไม่?", votesYes: 45, votesNo: 12, status: 'Active' },
    { id: 2, description: "ควรเพิ่มโบนัส KMT 20% สำหรับการทำสมาธิเกิน 60 นาทีต่อวันหรือไม่?", votesYes: 88, votesNo: 5, status: 'Active' },
];

export default function DaoVotingCard() {
    const [proposals, setProposals] = useState(mockProposals);
    const [votingStatus, setVotingStatus] = useState({});

    const handleVote = async (proposalId, choice) => {
        setVotingStatus(prev => ({ ...prev, [proposalId]: 'Voting...' }));
        
        try {
            // --- Web3 Integration Mockup ---
            // ในการทำงานจริง: 
            // 1. เรียกใช้ contract.methods.vote(proposalId, choice).send({ from: userAddress })
            await new Promise(resolve => setTimeout(resolve, 800));
            
            setProposals(prev => prev.map(p => {
                if (p.id === proposalId) {
                    return {
                        ...p,
                        votesYes: choice ? p.votesYes + 1 : p.votesYes,
                        votesNo: choice ? p.votesNo : p.votesNo + 1,
                    };
                }
                return p;
            }));
            
            setVotingStatus(prev => ({ ...prev, [proposalId]: `Voted ${choice ? 'YES' : 'NO'}` }));
        } catch (error) {
            console.error("DAO Voting failed:", error);
            setVotingStatus(prev => ({ ...prev, [proposalId]: 'Error voting' }));
        }
    };

    return (
        <div className="p-6 bg-white shadow-xl rounded-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">⚖️</span> Decentralized Governance (DAO)
            </h3>
            <div className="space-y-6">
                {proposals.map(p => (
                    <div key={p.id} className="border p-4 rounded-lg bg-gray-50">
                        <p className="font-medium text-lg text-indigo-700">{p.description}</p>
                        <div className="mt-3 flex justify-between items-center text-sm">
                            <div className="space-x-4">
                                <span className="text-green-600 font-bold">✅ Yes: {p.votesYes}</span>
                                <span className="text-red-600 font-bold">❌ No: {p.votesNo}</span>
                            </div>
                            
                            {votingStatus[p.id] && votingStatus[p.id].includes('Voted') ? (
                                <span className="text-sm text-gray-500">{votingStatus[p.id]}</span>
                            ) : (
                                <div className="space-x-2">
                                    <button 
                                        onClick={() => handleVote(p.id, true)} 
                                        className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm transition"
                                        disabled={votingStatus[p.id] === 'Voting...'}
                                    >
                                        โหวต ใช่
                                    </button>
                                    <button 
                                        onClick={() => handleVote(p.id, false)} 
                                        className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition"
                                        disabled={votingStatus[p.id] === 'Voting...'}
                                    >
                                        โหวต ไม่
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
