// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// ใช้ OpenZeppelin Governor หรือ AAVEDAO สำหรับโปรเจกต์จริง
// นี่คือ DAO Mockup สำหรับการตัดสินใจเชิงจริยธรรม (Ethical Proposals)

contract PutthochainDAO {
    // โครงสร้างสำหรับข้อเสนอเชิงจริยธรรม
    struct Proposal {
        uint256 id;
        string description;
        uint256 voteCountYes;
        uint256 voteCountNo;
        bool isExecuted;
        address creator;
    }
    
    // mapping เพื่อติดตามการโหวตของผู้ใช้แต่ละคนต่อข้อเสนอแต่ละข้อ
    mapping(uint256 => mapping(address => bool)) hasVoted; 
    
    Proposal[] public proposals;
    uint256 public nextProposalId = 1;
    
    // ต้องมี Karma Token เพื่อใช้เป็น Voting Power ในโปรเจกต์จริง
    // address public karmaTokenAddress; 
    
    event ProposalCreated(uint256 id, address creator);
    event Voted(uint256 id, address voter, bool choice);
    event ProposalExecuted(uint256 id);
    
    // ฟังก์ชันสร้างข้อเสนอใหม่ (เช่น การเปลี่ยนกฎ Karma Engine)
    function createProposal(string memory _description) public {
        proposals.push(Proposal({
            id: nextProposalId,
            description: _description,
            voteCountYes: 0,
            voteCountNo: 0,
            isExecuted: false,
            creator: msg.sender
        }));
        emit ProposalCreated(nextProposalId, msg.sender);
        nextProposalId++;
    }
    
    // ฟังก์ชันโหวต
    function vote(uint256 _proposalId, bool _voteYes) public {
        require(_proposalId > 0 && _proposalId < nextProposalId, "Invalid proposal ID");
        require(!hasVoted[_proposalId][msg.sender], "Already voted on this proposal");
        
        hasVoted[_proposalId][msg.sender] = true;
        
        if (_voteYes) {
            proposals[_proposalId - 1].voteCountYes++;
        } else {
            proposals[_proposalId - 1].voteCountNo++;
        }
        
        emit Voted(_proposalId, msg.sender, _voteYes);
    }
    
    // ฟังก์ชัน Execute (ใช้สำหรับข้อเสนอที่ผ่านการโหวต)
    function executeProposal(uint256 _proposalId) public {
        // ... (เงื่อนไขการผ่านโหวต เช่น Yes มากกว่า No 2:1)
        // ต้องตรวจสอบ Voting Power และผลโหวตจริง
        
        Proposal storage proposal = proposals[_proposalId - 1];
        require(!proposal.isExecuted, "Proposal already executed");
        
        // Mockup: สมมติว่าผ่านโหวตถ้า Yes > No
        if (proposal.voteCountYes > proposal.voteCountNo) {
            proposal.isExecuted = true;
            emit ProposalExecuted(_proposalId);
            // ในโปรเจกต์จริง ที่นี่คือการเรียกฟังก์ชันอื่นเพื่อทำการเปลี่ยนแปลงระบบ
        } else {
            revert("Proposal did not pass the quorum");
        }
    }
}
