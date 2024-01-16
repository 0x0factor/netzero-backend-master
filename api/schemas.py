from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class NFTMetadata(BaseModel):
    name: str = Field(..., description="The name of the NFT")
    description: str = Field(..., description="A description of the NFT")
    image: str = Field(..., description="The URL of the image for the NFT")
    attributes: List[dict] = Field([], description="A list of dictionaries containing attribute data for the NFT")
    external_url: str = Field(..., description="The external URL where the NFT can be viewed")


class PremineRequest(BaseModel):
    address: str
    kgCO2: float
    transactionsCount: int
    gasUsed: int
    highestBlockNumber: int
    lowestBlockNumber: int
    network: int
    current_time: Optional[datetime] = None

    def get_redis_key(self):
        return f'premine:{self.address}:{self.network}'


class PremineResponse(BaseModel):
    hbarValue: float
    contractAddress: str
    nftTokenId: str
    hashscan_url: str


class TreasuryAsset(BaseModel):
    symbol: str
    address: str
    balance: str
    pct: str
    price: str


class TreasuryHolders(BaseModel):
    address: str
    pending_votes: int
    investment: int


class TreasuryProjects(BaseModel):
    id: int
    title: str
    n_votes: int
    location: str
    description: str
    color: str
    share_pct: str


class TreasuryResponse(BaseModel):
    treasury_projects: List[TreasuryProjects]
    chainId: int
    totalInvestment: int = 0
    carbonOffsetPotential: int = 0
    carbonSequestered: int = 0
    holders: List[TreasuryHolders] = []
