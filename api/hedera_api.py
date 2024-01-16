import os
import random

from dotenv import load_dotenv
import requests
from web3 import Web3

from constants import daoAbi

load_dotenv()


BASE_URL = "https://previewnet.mirrornode.hedera.com/api/v1"
w3 = Web3(Web3.HTTPProvider(os.environ['HEDERA_PREVIEWNET_RPC']))

def get_random_hex_color():
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    return hex_number


def make_get(endpoint):
    response = requests.get(f'{BASE_URL}{endpoint}')
    return response.json()

def get_block_number() -> int:
    blocks = make_get('/blocks')
    return int(blocks['blocks'][0]['number'])

def get_projects_info(contract_address: str) -> list:
    contract = w3.eth.contract(address=contract_address, abi=daoAbi)
    names, votes, locations, descriptions = contract.functions.getProjects().call()
    project_shares = contract.functions.getProjectShares().call()
    objects = []
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    for idx, (name, vote, location, description, project_share) in enumerate(zip(names, votes, locations, descriptions, project_shares)):
        color = colors[idx] if idx < len(colors) else get_random_hex_color()
        object = {
            'id': idx,
            'title': name,
            'n_votes': vote,
            'location': location,
            'description': description,
            'color': color,
            'share_pct': project_share
        }
        objects.append(object)
    
    return objects

def get_investor_info(contract_address: str) -> list:
    contract = w3.eth.contract(address=contract_address, abi=daoAbi)
    
    objects = []
    
    _addresses, _votes, _investments = contract.functions.getInvestorsInfo().call()
    
    added = set()
    
    for idx, (address, pending_votes, investment) in enumerate(zip(_addresses, _votes, _investments)):
        if address not in added:
            object = {
                'address': address,
                'pending_votes': pending_votes,
                'investment': investment
            }
            objects.append(object)
            added.add(address)
    
    return objects


def get_total_investment(contract_address: str) -> int:
    contract = w3.eth.contract(address=contract_address, abi=daoAbi)
    return contract.functions.getTotalInvestment().call()


if __name__ == '__main__':
    projects = get_projects_info("0x3eAA0917966954a14D9F1874da8DceB015B239c5")
    print(projects)

