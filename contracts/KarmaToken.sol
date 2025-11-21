// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract KarmaToken is ERC20, Ownable {
    // กำหนดชื่อ (Karma Token) และสัญลักษณ์ (KMT)
    constructor() ERC20("KarmaToken", "KMT") Ownable(msg.sender) {
        // สามารถ mint token เริ่มต้นได้ถ้าต้องการ
    }

    // ฟังก์ชันสำคัญ: ให้ Backend (Karma Engine) สามารถ Mint Token ให้ผู้ใช้ได้
    // เฉพาะ Owner (Admin/DAO address) เท่านั้นที่เรียกใช้ได้
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
    
    // ฟังก์ชันเพิ่มเติม: สำหรับ DAO ในการเผา Token (ถ้าจำเป็น)
    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
}
