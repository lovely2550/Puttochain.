from web3 import Web3

# ตัวอย่างเชื่อม Polygon Mainnet (ใช้ Infura หรือ Alchemy)
RPC_URL = "https://polygon-rpc.com"  # เปลี่ยนเป็น RPC ของคุณ
PRIVATE_KEY = "YOUR_PRIVATE_KEY"     # ใส่ Private Key ของคุณ
TO_ADDRESS = "0xRecipientAddress"    # ใส่ address ผู้รับ
TOKEN_ADDRESS = "0xKarmaTokenAddress" # ใส่ address KarmaToken contract

w3 = Web3(Web3.HTTPProvider(RPC_URL))

account = w3.eth.account.from_key(PRIVATE_KEY)
nonce = w3.eth.get_transaction_count(account.address)

# ตัวอย่าง ERC20 ABI แบบ minimal
erc20_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

token_contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=erc20_abi)

# สร้าง Transaction
tx = token_contract.functions.transfer(TO_ADDRESS, 10 * 10**18).build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gas': 100000,
    'gasPrice': w3.to_wei('2', 'gwei')
})

# ลงนาม Transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

# ส่ง Transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

print("Transaction sent! TX Hash:", tx_hash.hex())