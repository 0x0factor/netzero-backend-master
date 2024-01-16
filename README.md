# NetZero DAO (by team HoraFeliz)

> Offset on-chain emissions using HBAR (the native Hedera currency) and invest in on-ground carbon projects

![image](https://github.com/gautamp8/netzero-dao/assets/10217535/5a35d336-f33e-40d0-b4b1-7a4e75fc1e02)


## Try it out

See the project explanation video at: https://youtu.be/av83zaqHCIc

[![NetZero Demo](https://img.youtube.com/vi/av83zaqHCIc/1.jpg)](https://www.youtube.com/watch?v=av83zaqHCIc)


Check the deployed app at https://netzero-dao.vercel.app/


## About the code

This repo contains the Backend-end for the project. The code primarily has two parts; the smart contracts, and the API server. The smart contract part predominantly uses Hardhat framework and hashgraph-sdk. The API server part uses FastAPI and requires Redis for storage.

The frontend code can be accessed in a different repo [here](https://github.com/gautamp8/netzero-dao).

### Architecture

Here's what the current architecture looks like

![image](/images/architecture.svg)

## Instructions to run

To get started with this project, clone this repo and follow the commands below

### Smart contracts

#### One-time setup

- Run `npm install` at the root of your directory to install the dependencies. It is recommended you use node v18 or higher.
- Create a `.env` referring to `sample.env` file.
- Run `npx hardhat compile` to compile the smart contracts.

#### Recurring Instructions

We've used different scripts for different purposes. Feel free to check those and run them using hardhat. For example, for deploying DAO using the `deployDAO.js` script you can run `npx hardhat run scripts/deployDAO.js --network hedera`.


### API server

#### One-time setup

- Create a `api/.env` file referring to the sample `api/sample.env` file.
- Create a virtualenv (optional)
- Install the dependencies using `pip install -r requirements.txt`

#### Recurring Instructions

- API server can be run using `./start_api.bash 7777` command. Where 7777 is the local port on which the server would be listening to.

PS: This is our submission for Beyond Blockchain: Hashgraph Hackathon, we intend to take this project further post-hackathon.
