from fastapi.testclient import TestClient
from puttochain.models import User, DaoProposal
from main import app # จำเป็นต้อง Import main เพื่อให้ TestClient ทำงาน
import pytest

# ข้อมูล Mockup สำหรับการเรียก API
TEST_WALLET = "0xTestWallet001ForAPI"
TEST_ADMIN_WALLET = "0xAdminWallet1" # ต้องอยู่ใน ADMIN_WALLETS list ใน auth.py

JOURNAL_DATA = {
    "user_wallet_address": TEST_WALLET,
    "content": "ทดสอบการบันทึก Karma Engine และ IPFS",
    "is_good_deed": True,
    "meditation_minutes": 10
}

# --- 1. ทดสอบ Journal/Karma API ---

def test_create_journal_and_karma_update(client: TestClient, db_session):
    """ทดสอบการสร้าง Journal และการคำนวณ Karma"""
    
    # 1. การเรียก POST API
    response = client.post("/journals/", json=JOURNAL_DATA)
    
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert data["level"] == "Practitioner" # เริ่มต้น 0 + 10 (Good Deed) + 2 (Meditation) = 12

    # 2. ตรวจสอบใน Database
    user = db_session.query(User).filter(User.wallet_address == TEST_WALLET).first()
    assert user is not None
    assert user.karma_score > 0
    assert user.total_meditation_minutes == 10
    
    journal_entry = user.journals[0]
    assert "Qm" in journal_entry.ipfs_hash # ต้องมี hash ของ IPFS ถูกบันทึก
    assert journal_entry.karma_change == 12

def test_get_karma_status_success(client: TestClient, db_session):
    """ทดสอบการดึงสถานะ Karma ที่มีอยู่แล้ว"""
    # ต้องสร้าง User ก่อน
    user = User(wallet_address=TEST_WALLET, karma_score=200)
    db_session.add(user)
    db_session.commit()
    
    response = client.get(f"/karma/{TEST_WALLET}")
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 200
    assert data["level"] == "Practitioner"

def test_get_karma_status_not_found(client: TestClient):
    """ทดสอบเมื่อ User ไม่พบใน DB"""
    response = client.get("/karma/0xNonExistingUser")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

# --- 2. ทดสอบ DAO API ---

@pytest.fixture
def admin_user(db_session):
    """Fixture สำหรับสร้าง Admin User ใน DB"""
    # Mockup: Wallet นี้ถือว่าเป็น Admin ตาม logic ใน auth.py
    user = User(wallet_address=TEST_ADMIN_WALLET, karma_score=1000)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_create_dao_proposal_admin_success(client: TestClient, admin_user):
    """ทดสอบการสร้าง Proposal โดยใช้ Admin Token"""
    
    # Override Auth เพื่อใช้ Token ของ Admin
    client.app.dependency_overrides[app.dependency_overrides[get_current_user_wallet]] = lambda: admin_user
    
    proposal_data = {"title": "Test Proposal", "description": "Details"}
    
    # ต้องส่ง API Token ของ Admin
    response = client.post(
        "/dao/proposals/", 
        json=proposal_data, 
        headers={"X-API-Token": TEST_ADMIN_WALLET}
    )
    assert response.status_code == 201
    assert "proposal_id" in response.json()

def test_create_dao_proposal_unauthorized(client: TestClient):
    """ทดสอบการสร้าง Proposal โดยไม่มีสิทธิ์"""
    proposal_data = {"title": "Test Proposal", "description": "Details"}
    # ส่ง Token ที่ไม่ใช่ Admin
    response = client.post(
        "/dao/proposals/", 
        json=proposal_data, 
        headers={"X-API-Token": TEST_WALLET} 
    )
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]

def test_get_active_proposals(client: TestClient, db_session):
    """ทดสอบการดึงรายการ Proposal"""
    proposal = DaoProposal(title="Active Test", description="Desc")
    db_session.add(proposal)
    db_session.commit()
    
    response = client.get("/dao/proposals/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["title"] == "Active Test"
