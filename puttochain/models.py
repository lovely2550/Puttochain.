# ... (User และ JournalEntry Models เดิม) ...

class DaoProposal(Base):
    """
    ตารางสำหรับข้อเสนอการโหวตเชิงจริยธรรมของ DAO
    """
    __tablename__ = "dao_proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Vote Counts
    votes_yes = Column(Integer, default=0)
    votes_no = Column(Integer, default=0)
    
    # Status
    is_executed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
