// scripts/deploy.js

const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // --- 1. Deploy KarmaToken (KMT) ---
  const KarmaToken = await hre.ethers.getContractFactory("KarmaToken");
  const initialSupply = hre.ethers.parseUnits("1000000", 18); // 1 ล้าน KMT (สำหรับ Admin/Initial Pool)
  const karmaToken = await KarmaToken.deploy(initialSupply);
  
  await karmaToken.waitForDeployment();
  const kmtAddress = await karmaToken.getAddress();
  
  console.log("✅ KarmaToken deployed to:", kmtAddress);

  // --- 2. Deploy PutthochainDAO (ต้องใส่ KMT Address เป็น Constructor Argument) ---
  const PutthochainDAO = await hre.ethers.getContractFactory("PutthochainDAO");
  const dao = await PutthochainDAO.deploy(kmtAddress);

  await dao.waitForDeployment();
  const daoAddress = await dao.getAddress();

  console.log("✅ PutthochainDAO deployed to:", daoAddress);

  // --- 3. ตั้งค่า Ownerships/Permissions ที่จำเป็น ---
  
  // ในระบบจริง: ต้องตั้งค่า Backend Contract (ที่ทำหน้าที่ Mint KMT) ให้เป็น Minters
  // karmaToken.transferOwnership(ADMIN_CONTRACT_ADDRESS); // หรือตั้งค่า Role-based access control
  
  console.log("\nDeployment Complete!");
  console.log("-----------------------------------------");
  console.log("KMT Address (Update in .env):", kmtAddress);
  console.log("DAO Address (Update in .env):", daoAddress);
  console.log("-----------------------------------------");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
