// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");

async function main() {
  const NetZeroNFT = await hre.ethers.getContractFactory("NetZeroNFT");
//   const netZeroNFT = await NetZeroNFT.deploy({
//     gasLimit: 5000000
//   });
    const netZeroNFT = await NetZeroNFT.attach("0x09558398a2c7829b0411ea5e66a5f577bf10dca5");

  console.log("NetZeroNFT deployed to: " + netZeroNFT.address);

  var txn = await netZeroNFT.mint("0x0000000000000000000000000000000000e42c9b", {
    gasLimit: 15000000
  });
  await txn.wait();
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
