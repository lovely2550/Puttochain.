// hardhat.config.js

require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config(); // เพื่อ Load Private Key และ RPC URL

const POLYGON_RPC_URL = process.env.POLYGON_RPC_URL;
const ADMIN_PRIVATE_KEY = process.env.ADMIN_PRIVATE_KEY;

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.24", // ใช้ Solidity version ล่าสุด
  networks: {
    // ใช้สำหรับ Development และ Testing ภายในเครื่อง
    hardhat: {},
    // สำหรับ Deploy บน Polygon Testnet/Mainnet
    polygon: {
      url: POLYGON_RPC_URL,
      accounts: [ADMIN_PRIVATE_KEY],
      chainId: 137, // 137 สำหรับ Polygon Mainnet, 80001 สำหรับ Mumbai Testnet
    }
  },
  etherscan: {
    // สำหรับ Verify Contract บน Polygonscan
    apiKey: process.env.POLYGANSAN_API_KEY
  }
};
