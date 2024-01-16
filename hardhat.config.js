require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config()

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  defaultNetwork: 'localhost',
  solidity: "0.8.17",
  settings: {
    optimizer: {
      enabled: true,
      runs: 1000
    }
  },
  networks: {
    localhost: {
      forking: {
        url: process.env.HEDERA_RPC,
        gas: 21000000,
      }
    },
    hedera: {
      url: process.env.HEDERA_RPC,
      accounts: [process.env.PRIVATE_KEY_1, process.env.PRIVATE_KEY_2, process.env.PRIVATE_KEY_3],
      gas: 21000000,
    },
    hedera_local: {
      url: process.env.HEDERA_LOCAL_RPC,
      accounts: [process.env.PRIVATE_KEY_1, process.env.PRIVATE_KEY_2, process.env.PRIVATE_KEY_3],
      gas: 21000000,
    },
    hedera_previewnet: {
      url: process.env.HEDERA_PREVIEWNET_RPC,
      accounts: [process.env.PRIVATE_KEY_1, process.env.PRIVATE_KEY_2, process.env.PRIVATE_KEY_3],
      gas: 21000000,
      
    }
  }
};
