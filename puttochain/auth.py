from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from typing import Optional

# กำหนด header ที่ใช้ส่ง API Key (e.g., X-API-Token: <token>)
API_KEY_NAME = "X-API-Token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Mockup: In a real system, the token is generated on user login/signature
# and stored securely. Here, we assume the token is the user's wallet address 
# or a derived key for simplicity.

async def get_current_user_wallet(
    api_token: str = Security(api_key_header),
    db: Session = Depends(get_db)
) -> User:
    """
    ตรวจสอบ API Token และคืนค่า User object ที่เชื่อมโยง
    """
    if not api_token:
        raise HTTPException(status_code=401, detail="Missing API Token")

    # ในระบบจริง: Token จะถูก hash และค้นหาในตาราง User/Token
    # Mockup: เราถือว่า API Token คือ Wallet Address (เพื่อความง่ายในการทดสอบ)
    user = db.query(User).filter(User.wallet_address == api_token).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid API Token or User not found")
        
    return user

async def get_admin_user(current_user: User = Depends(get_current_user_wallet)):
    """
    ตรวจสอบว่าเป็น Admin หรือไม่ (สำหรับ Endpoint ที่มีสิทธิ์พิเศษ)
    """
    # ในระบบจริง: อาจมี field is_admin ในตาราง User
    # Mockup: สมมติว่า Wallet Address บางอันเป็น Admin
    ADMIN_WALLETS = ["0xAdminWallet1", "0xAdminWallet2"]
    
    if current_user.wallet_address not in ADMIN_WALLETS:
        raise HTTPException(status_code=403, detail="Not authorized to perform this action (Admin access required)")
        
    return current_user
