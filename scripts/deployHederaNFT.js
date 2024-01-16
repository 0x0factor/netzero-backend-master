require("dotenv").config();
const {
  AccountId,
  PrivateKey,
  Client,
  Hbar,
  TokenCreateTransaction,
  TokenType,
  TokenSupplyType,
  TokenMintTransaction,
  TransferTransaction,
  AccountBalanceQuery,
  TokenAssociateTransaction,
} = require("@hashgraph/sdk");

const operatorId = AccountId.fromString(process.env.OPERATOR_ID);
const operatorKey = PrivateKey.fromString(process.env.OPERATOR_PVKEY);
const treasuryId = AccountId.fromString(process.env.TREASURY_ID);
const treasuryKey = PrivateKey.fromString(process.env.TREASURY_PVKEY);
const aliceId = AccountId.fromString(process.env.ALICE_ID);
const aliceKey = PrivateKey.fromString(process.env.ALICE_PVKEY);
const client = Client.forTestnet().setOperator(operatorId, operatorKey);
const supplyKey = PrivateKey.generate();

async function createNFT() {
  const nftCreate = await new TokenCreateTransaction()
    .setTokenName("NetZero NFT")
    .setTokenSymbol("NZT")
    .setTokenType(TokenType.NonFungibleUnique)
    .setDecimals(0)
    .setInitialSupply(0)
    .setTreasuryAccountId(treasuryId)
    .setSupplyKey(supplyKey)
    .freezeWith(client);

  const nftCreateTxSign = await nftCreate.sign(treasuryKey);
  const nftCreateSubmit = await nftCreateTxSign.execute(client);
  const nftCreateRx = await nftCreateSubmit.getReceipt(client);
  const tokenId = nftCreateRx.tokenId;
  console.log(`- Created NFT with Token ID: ${tokenId} \n`);

  return tokenId;
}

async function mintNFTs(tokenId) {
  const maxTransactionFee = new Hbar(20);
  const CID = [
    Buffer.from(
      "https://c555-2401-4900-1cb9-cbd0-f41c-5741-4b28-e677.ngrok-free.app/metadata/testnet/0"
    ),
  ];

  const mintTx = new TokenMintTransaction()
    .setTokenId(tokenId)
    .setMetadata(CID)
    .setMaxTransactionFee(maxTransactionFee)
    .freezeWith(client);

  const mintTxSign = await mintTx.sign(supplyKey);
  const mintTxSubmit = await mintTxSign.execute(client);
  const mintRx = await mintTxSubmit.getReceipt(client);

  console.log(
    `- Created NFT ${tokenId} with serial: ${mintRx.serials[0].low} \n`
  );
}

async function associateAliceToNFT(tokenId) {
  const associateAliceTx = await new TokenAssociateTransaction()
    .setAccountId(aliceId)
    .setTokenIds([tokenId])
    .freezeWith(client)
    .sign(aliceKey);

  const associateAliceTxSubmit = await associateAliceTx.execute(client);
  const associateAliceRx = await associateAliceTxSubmit.getReceipt(client);

  console.log(
    `- NFT association with Alice's account: ${associateAliceRx.status}\n`
  );
}

async function transferNFT(tokenId) {
  const tokenTransferTx = await new TransferTransaction()
    .addNftTransfer(tokenId, 1, treasuryId, aliceId)
    .freezeWith(client)
    .sign(treasuryKey);

  const tokenTransferSubmit = await tokenTransferTx.execute(client);
  const tokenTransferRx = await tokenTransferSubmit.getReceipt(client);

  console.log(
    `\n- NFT transfer from Treasury to Alice: ${tokenTransferRx.status} \n`
  );
}

async function main() {
  const tokenId = await createNFT();
  await mintNFTs(tokenId);
  // await associateAliceToNFT(tokenId);
  // await transferNFT(tokenId);
}

main();
