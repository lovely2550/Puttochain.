// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PutthochainDAO
 * @dev DAO Contract สำหรับการกำกับดูแลกฎเกณฑ์ของ Karma Engine โดยใช้ KMT Token
 */
contract PutthochainDAO is Ownable {
    
    // --- State Variables ---
    
    // Address ของ Karma Token (KMT)
    IERC20 public immutable karmaToken;

    // โครงสร้างสำหรับจัดเก็บข้อเสนอ
    struct Proposal {
        uint256 id;
        string title;
        string description;
        uint256 voteStartTime;
        uint256 voteEndTime;
        uint256 votesFor;
        uint256 votesAgainst;
        bool executed;
        // Mockup: สำหรับฟังก์ชันที่ต้องการเรียกใช้เมื่อผ่านการโหวต
        address payable target;
        bytes callData;
    }
    
    // การจัดเก็บข้อเสนอทั้งหมด
    Proposal[] public proposals;
    
    // Mapping: proposalId => voterAddress => hasVoted (True/False)
    mapping(uint256 => mapping(address => bool)) public hasVoted;
    
    // --- Events ---
    event ProposalCreated(uint256 proposalId, address proposer, string title);
    event Voted(uint256 proposalId, address voter, bool support, uint256 voteWeight);
    event ProposalExecuted(uint256 proposalId);

    // --- Constructor ---
    constructor(address _karmaTokenAddress) Ownable(msg.sender) {
        karmaToken = IERC20(_karmaTokenAddress);
    }
    
    // --- Core DAO Functions ---

    /**
     * @notice อนุญาตให้ Owner (Backend/Admin Wallet) สร้างข้อเสนอใหม่
     * @param _title หัวข้อข้อเสนอ
     * @param _description รายละเอียด
     * @param _votingPeriod ระยะเวลาโหวตเป็นวินาที
     * @param _target Mockup: Contract address ที่จะเรียกใช้ (ถ้า Proposal ผ่าน)
     * @param _callData Mockup: ข้อมูลฟังก์ชันที่จะเรียกใช้ (ABI Encoded)
     */
    function createProposal(
        string memory _title,
        string memory _description,
        uint256 _votingPeriod,
        address payable _target,
        bytes memory _callData
    ) public onlyOwner returns (uint256) {
        require(_votingPeriod > 0, "Voting period must be greater than zero");
        
        uint256 newId = proposals.length;
        
        proposals.push(Proposal({
            id: newId,
            title: _title,
            description: _description,
            voteStartTime: block.timestamp,
            voteEndTime: block.timestamp + _votingPeriod,
            votesFor: 0,
            votesAgainst: 0,
            executed: false,
            target: _target,
            callData: _callData
        }));

        emit ProposalCreated(newId, msg.sender, _title);
        return newId;
    }

    /**
     * @notice ให้ผู้ถือ KMT ลงคะแนนโหวตในข้อเสนอ
     * @param _proposalId ID ของข้อเสนอ
     * @param _support True สำหรับ 'Yes', False สำหรับ 'No'
     */
    function vote(uint256 _proposalId, bool _support) public {
        Proposal storage proposal = proposals[_proposalId];
        
        require(block.timestamp >= proposal.voteStartTime, "Voting has not started");
        require(block.timestamp <= proposal.voteEndTime, "Voting has ended");
        require(hasVoted[_proposalId][msg.sender] == false, "Already voted");
        
        // ใช้ KMT Balance เป็นน้ำหนักคะแนนโหวต (Token Balance at the moment of voting)
        uint256 voteWeight = karmaToken.balanceOf(msg.sender);
        require(voteWeight > 0, "Must hold KMT to vote");

        hasVoted[_proposalId][msg.sender] = true;

        if (_support) {
            proposal.votesFor += voteWeight;
        } else {
            proposal.votesAgainst += voteWeight;
        }
        
        emit Voted(_proposalId, msg.sender, _support, voteWeight);
    }

    /**
     * @notice นำข้อเสนอที่ผ่านการโหวตไปปฏิบัติ (Execute)
     * @param _proposalId ID ของข้อเสนอ
     */
    function executeProposal(uint256 _proposalId) public {
        Proposal storage proposal = proposals[_proposalId];
        
        require(block.timestamp > proposal.voteEndTime, "Voting is still active");
        require(proposal.votesFor > proposal.votesAgainst, "Proposal failed to pass");
        require(proposal.executed == false, "Proposal already executed");
        
        proposal.executed = true;

        // Mockup: การเรียกใช้ฟังก์ชันภายนอก (ในระบบจริงอาจเป็น Contract Upgrade หรือ Parameter Change)
        (bool success, ) = proposal.target.call(proposal.callData);
        require(success, "Execution failed");

        emit ProposalExecuted(_proposalId);
    }
}
