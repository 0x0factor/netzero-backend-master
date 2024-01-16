from datetime import datetime
import os
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
import uvicorn
from web3 import Web3

from constants import erc721abi, erc20abi
from logger import get_logger
import hedera_api
from schemas import NFTMetadata, PremineRequest, PremineResponse, TreasuryResponse
from utils import ErrorHandlerRoute

load_dotenv()
logger = get_logger(__name__)
r = redis.Redis()

app = FastAPI(
    title='NetZero API', description='', version='0.1',
)
app.router.route_class = ErrorHandlerRoute


CONTRACT_ADDRESS = "0x3eAA0917966954a14D9F1874da8DceB015B239c5"
PUBLIC_URL = 'https://c555-2401-4900-1cb9-cbd0-f41c-5741-4b28-e677.ngrok-free.app'
NFT_TOKEN_ID =  "0.0.229938"
CARBON_SEQUESTERED = 100


# TODO: This needs to be tuned
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

w3_mapping = {
    296: Web3(Web3.HTTPProvider(os.environ["HEDERA_TESTNET_RPC"])),
    297: Web3(Web3.HTTPProvider(os.environ["HEDERA_PREVIEWNET_RPC"])),
}


hbar_price = 0.05
one_carbon_tonne_price = 9.5
one_usd_carbon_tonne = 1 / one_carbon_tonne_price
one_hbar_offset = 0.05 * one_usd_carbon_tonne
one_carbon_tonne_hbar = one_carbon_tonne_price / hbar_price


def get_nft_owner(network, tokenId, contract_address):
    w3 = w3_mapping[network]
    # Load the ERC721 contract
    contract = w3.eth.contract(address=contract_address, abi=erc721abi)
    # Get the NFT owner of the tokenId
    owner = contract.functions.ownerOf(tokenId).call()
    return owner


def get_nft_total_supply(network, contract_address):
    w3 = w3_mapping[network]
    # Load the ERC721 contract
    contract = w3.eth.contract(address=contract_address, abi=erc721abi)
    # Get the total supply of the NFT
    total_supply = contract.functions.totalSupply().call()
    return total_supply


def get_nft_owned_if_any(network, contract_address, address):
    w3 = w3_mapping[network]
    # Load the ERC721 contract
    contract = w3.eth.contract(address=contract_address, abi=erc721abi)
    # Check if the user owns any nft
    balance = contract.functions.balanceOf(address).call()
    # If the users owns, find the tokenID
    if float(balance):
        # find the tokenIDs owned and return the first one
        token_id = contract.functions.tokenOfOwnerByIndex(address, 0).call()
        return token_id
    
    return None


def get_erc20_balance(network, contract_address, address):
    w3 = w3_mapping[network]
    # load the ERC20 contract
    contract = w3.eth.contract(address=contract_address, abi=erc20abi)
    # Get the balance of the address
    balance = contract.functions.balanceOf(address).call()
    return balance


def send_validation_error(detail):
    logger.error(f"Validation error: {detail}")
    raise HTTPException(status_code=422, detail=detail)


def validate_body(body) -> bool:
    return True


@app.get('/')
async def status():
    return 'OK'


@app.get('/m/{network}/{tokenId}', response_model=NFTMetadata)
async def get_metadata(network: str, tokenId: str):
    
    if network == 'mainnet':
        network = 295
    elif network == 'testnet':
        network = 296
    elif network == 'p':
        network = 297
    
    owner = tokenId
    metadata_key = f'premine:{owner}:{network}'
    metadata = PremineRequest(**json.loads(r.get(metadata_key)))
    
    blockNumber = hedera_api.get_block_number()
    
    if metadata.current_time is None:
        metadata.current_time = datetime.now()
    
    return NFTMetadata(
        name=f"🌎 NetZero NFT of {owner}",
        description="NetZero is a non-fungible token that represent the amount of carbon emissions retired by a wallet address.",
        image="https://media.discordapp.net/attachments/953846124471529512/1121510485964095538/Zerocarbon_NFT_2.gif",
        attributes=[
            {
                "trait_type": "🫧 CO2 Emissions",
                "value": f"{metadata.kgCO2} kg"
            },
            {
                "trait_type": "🔢 Transactions Offseted",
                "value": metadata.transactionsCount
            },
            {
                "trait_type": "⛽ Lifetime Gas Used",
                "value": f"{metadata.gasUsed} gas"
            },
            {
                "trait_type": "#️⃣  Rank",
                "value": 1,
                "type": "number",
                "max_value": 5
            },
            {
                "display_type": "date",
                "trait_type": "🪴 Date of minting",
                "value": int(metadata.current_time.timestamp())
            },
            {
                "display_type": "date",
                "trait_type": "⌛ Last Refreshed",
                "value": int(datetime.now().timestamp())
            },
            {
                "display_type": "boost_percentage",
                "trait_type": "Offset Percentage",
                "value": 100
            },
            {
                "trait_type": "⏮️ Last txn Block#",
                "value": metadata.highestBlockNumber,
                "max_value": blockNumber
            },
            {
                "trait_type": "🥇 First txn Block#",
                "value": metadata.lowestBlockNumber,
                "max_value": blockNumber
            }
        ],
        external_url=f"{PUBLIC_URL}/{tokenId}"
    )


@app.post('/premine', response_model=PremineResponse)
async def get_metadata(request: PremineRequest):
    print(f"Premine request: {request}")
    # request.current_time = datetime.now() # this is not json serializable
    r.set(request.get_redis_key(), json.dumps(request.dict()))
    
    hbarCIValue = one_carbon_tonne_hbar * request.kgCO2 / 1000
    return PremineResponse(
        hbarValue=int(hbarCIValue),
        contractAddress=CONTRACT_ADDRESS,
        nftTokenId=NFT_TOKEN_ID,
        hashscan_url=f"https://hashscan.io/previewnet/token/{NFT_TOKEN_ID}"
    )


# 49965


@app.get('/treasury', response_model=TreasuryResponse)
def get_treasury(chainId: int):
    projects_info = hedera_api.get_projects_info(CONTRACT_ADDRESS)
    total_investment = hedera_api.get_total_investment(CONTRACT_ADDRESS)
    carbon_offset_potential = total_investment * one_hbar_offset * 1000 / (10 ** 9)
    
    holders_info = hedera_api.get_investor_info(CONTRACT_ADDRESS)
    
    return TreasuryResponse(
        treasury_projects=projects_info,
        chainId=chainId,
        totalInvestment=total_investment,
        carbonOffsetPotential=int(carbon_offset_potential),
        carbonSequestered=CARBON_SEQUESTERED,
        holders=holders_info
    )
        

@app.on_event('startup')
async def startup():
    pass
# 

if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run('main:app', host="0.0.0.0", port=8888, reload=True)
