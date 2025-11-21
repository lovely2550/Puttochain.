import json
import os
from web3 import Web3
from dotenv import load_dotenv

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

# --- ข้อมูลที่จำเป็น ---
ADMIN_PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY")
KARMA_TOKEN_ADDRESS = os.getenv("KARMA_TOKEN_ADDRESS")
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL")

# --- ABI ของ KarmaToken ---
# ในโปรเจกต์จริง คุณจะต้องคัดลอก ABI (Application Binary Interface) 
# ของ contract KarmaToken.sol ที่ Compile แล้วมาใส่ที่นี่
KARMA_TOKEN_ABI = [
    # Function signature สำหรับ mint (ต้องมี)
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "mint",
        "outputs": [],
        "type": "function"
    },
    # Function signature สำหรับ decimals (มักจะจำเป็น)
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
]

class BlockchainIntegrator:
    """
    Handles all interactions with the Polygon Blockchain (e.g., Minting KarmaToken).
    """
    def __init__(self):
        # 1. เชื่อมต่อ Web3
        self.w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Polygon RPC node.")
        
        # 2. ตั้งค่า Admin Wallet
        self.admin_account = self.w3.eth.account.from_key(ADMIN_PRIVATE_KEY)
        
        # 3. โหลด Contract
        self.token_contract = self.w3.eth.contract(address=KARMA_TOKEN_ADDRESS, abi=KARMA_TOKEN_ABI)
        
        # 4. กำหนด Decimals สำหรับการคำนวณ Token
        # self.decimals = self.token_contract.functions.decimals().call() 
        self.decimals = 18 # Mockup: Assume 18 decimals

    def mint_karma_token(self, recipient_wallet: str, amount_of_karma: int):
        """
        Mints Karma Tokens (KMT) and sends them to the user's wallet.
        
        :param recipient_wallet: User's Polygon wallet address.
        :param amount_of_karma: Amount of KMT to mint (as a whole number).
        """
        try:
            # แปลงจำนวนโทเคนให้อยู่ในรูปแบบ Wei (ตาม decimals ของ ERC20)
            token_amount_wei = amount_of_karma * (10 ** self.decimals)
            
            # 1. สร้าง Transaction Call
            nonce = self.w3.eth.get_transaction_count(self.admin_account.address)
            
            mint_txn = self.token_contract.functions.mint(
                recipient_wallet, 
                token_amount_wei
            ).build_transaction({
                'from': self.admin_account.address,
                'nonce': nonce,
                'gas': 200000, # กำหนด Gas Limit
                'gasPrice': self.w3.eth.gas_price # ใช้ Gas Price ปัจจุบันของเครือข่าย
            })

            # 2. ลงนาม (Sign) Transaction
            signed_txn = self.w3.eth.account.sign_transaction(mint_txn, private_key=ADMIN_PRIVATE_KEY)

            # 3. ส่ง Transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            print(f"[Blockchain] Mint Tx Hash: {self.w3.to_hex(tx_hash)}")
            print(f"[Blockchain] Waiting for transaction receipt...")
            
            # รอการยืนยัน Transaction (Optional)
            # receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            # print(f"[Blockchain] Transaction confirmed! Block: {receipt.blockNumber}")

        except Exception as e:
            print(f"[Blockchain ERROR] Failed to mint token: {e}")
            # ควรมี Logic การชดเชย (Revert) หรือการบันทึก Error Log

# Example Usage (ใช้ใน main.py)
# blockchain_integrator = BlockchainIntegrator()
# blockchain_integrator.mint_karma_token(user_wallet_address, karma_change)
