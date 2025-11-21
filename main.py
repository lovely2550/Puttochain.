# main.py (เพิ่ม Pydantic Schema)
# ... (Pydantic Schemas เดิม) ...

class ProposalCreate(BaseModel):
    title: str
    description: str

class ProposalVote(BaseModel):
    proposal_id: int
    vote: bool # True = Yes, False = No

# --- API Endpoints สำหรับ DAO ---

@app.post("/dao/proposals/", tags=["DAO Governance"], status_code=201)
async def create_dao_proposal(
    proposal_in: ProposalCreate,
    admin_user: User = Depends(get_admin_user), # <--- ต้องเป็น Admin เท่านั้นที่สร้างได้
    db: Session = Depends(get_db)
):
    """สร้างข้อเสนอ DAO ใหม่ (Admin Only)"""
    db_proposal = DaoProposal(
        title=proposal_in.title,
        description=proposal_in.description
    )
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return {"message": "Proposal created successfully", "proposal_id": db_proposal.id}

@app.get("/dao/proposals/", tags=["DAO Governance"])
def get_active_proposals(db: Session = Depends(get_db)):
    """ดึงข้อเสนอที่กำลัง Active ทั้งหมด"""
    proposals = db.query(DaoProposal).filter(DaoProposal.is_active == True).all()
    return proposals

@app.post("/dao/vote/", tags=["DAO Governance"])
async def vote_on_proposal(
    vote_in: ProposalVote,
    current_user: User = Depends(get_current_user_wallet), # <--- ต้อง Login ด้วย Token
    db: Session = Depends(get_db)
):
    """
    ลงคะแนนโหวตในข้อเสนอ (Mockup: ไม่ได้ตรวจสอบ KMT Token Balance)
    """
    proposal = db.query(DaoProposal).filter(DaoProposal.id == vote_in.proposal_id).first()
    
    if not proposal or not proposal.is_active:
        raise HTTPException(status_code=404, detail="Proposal not found or not active")
        
    # **Logic ที่สำคัญ:** ตรวจสอบว่าผู้ใช้เคยโหวตข้อเสนอนี้แล้วหรือไม่
    # ในระบบจริงต้องมีตาราง 'Vote' แยกเพื่อตรวจสอบ
    
    if vote_in.vote:
        proposal.votes_yes += 1
    else:
        proposal.votes_no += 1
        
    db.commit()
    
    # 📌 ส่วนนี้คือจุดที่ Backend ควรจะเรียก Smart Contract `vote(proposalId, choice)`
    print(f"[Blockchain MOCK] User {current_user.id} voted on Proposal {vote_in.proposal_id}")
    
    return {"message": "Vote recorded successfully"}
