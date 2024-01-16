const hre = require("hardhat");

async function main() {

  const projects = [
    {
        "project_name": "Kariba REDD+ Project",
        "location": "Zimbabwe",
        "description": "Prevents deforestation and wildlife extinction in northern Zimbabwe."
    },
    {
        "project_name": "Kasigau Corridor REDD+ Project",
        "location": "Kenya",
        "description": "Protects threatened forest habitats and wildlife in Kenya."
    },
    {
        "project_name": "Madre de Dios Amazon REDD",
        "location": "Peru",
        "description": "Preserves the biodiversity of the Amazon rainforest in Peru."
    },
    {
        "project_name": "Rimba Raya Biodiversity Reserve REDD",
        "location": "Indonesia",
        "description": "Protects endangered species and their habitats in Borneo."
    },
    {
        "project_name": "Alto Mayo Protected Forest REDD",
        "location": "Peru",
        "description": "Conserves the biodiversity of the Alto Mayo Protected Forest."
    }]
  const DAO = await hre.ethers.getContractFactory("DAO");
  // const dao = await DAO.attach("0x775B7d5CE0342DD34AcA70137bDadC4BC6FA5579");
  const dao = await DAO.deploy();
  await dao.deployed();
  console.log("DAO deployed to:", dao.address);

  // // loop over the projects and create
  for (let i = 0; i < projects.length; i++) {
    const project = projects[i];

    // add try catch logic here, if the statement fails wait for 5 seconds and retry
    while(true) {
      try {
        await dao.createProject(project.project_name, project.location, project.description, {
          gasLimit: 15000000
        });
        console.log(`Project ${i + 1} created`);
        break;
      } catch {
        console.log(`Error creating project ${i + 1}, retrying in 5 seconds`);
        await new Promise(r => setTimeout(r, 5000));
      }
    }
  }

  const onChainprojects = await dao.getProjects({gasLimit: 15000000 });
  console.log(`Projects: ${onChainprojects.toString()}`);

  // Get test accounts
  const [account3, account2, account1] = await hre.ethers.getSigners();

  // Invest from 2 different addresses
  await dao.connect(account1).invest({ value: hre.ethers.utils.parseEther("10"), gasLimit: 14000000 });
  await dao.connect(account2).invest({ value: hre.ethers.utils.parseEther("20"), gasLimit: 14000000 });

  
  const investedAmount1 = await dao.getInvestment(account1.address);
  console.log(`Invested amount for account 1: ${investedAmount1.toString()}`);
  const investedAmount2 = await dao.getInvestment(account2.address);
  console.log(`Invested amount for account 2: ${investedAmount2.toString()}`);


  dao.connect(account1).bulkVote([0, 2, 3, 4], [2000, 5000, 1000, 500], {gasLimit: 15000000})
  console.log("Bulk Vote 1 done")

  dao.connect(account2).bulkVote([1, 2, 3], [5000, 1000, 500], {gasLimit: 15000000})
  console.log("Bulk Vote 2 done")

  // Vote for projects
  await dao.connect(account1).vote(0, 100, {gasLimit: 15000000});
  console.log("Vote 1.1 done")

  // this time add gaslimit 
  // await dao.connect(account1).vote(1, 200, {gasLimit: 15000000});
  // console.log("Vote 1.2 done")

  // await dao.connect(account2).vote(1, 300, {gasLimit: 15000000});
  // console.log("Vote 2.1 done")

  // await dao.connect(account2).vote(0, 400, {gasLimit: 15000000});
  // console.log("Vote 2.2 done")

  // const pendingVotes1 = await dao.getPendingVotes(account1.address);
  // console.log(`Pending votes for account 1: ${pendingVotes1.toString()}`);

  // const pendingVotes2 = await dao.getPendingVotes(account2.address);
  // console.log(`Pending votes for account 2: ${pendingVotes2.toString()}`);

  // Print project shares
  // for (let i = 0; i < 2; i++) {
  //   const share = await dao.getProjectShare(i);
  //   const quadraticShare = await dao.getProjectShareAsPerQuadraticVoting(i);
  //   console.log(`Project ${i + 1} share: ${share.toString()}%, quadratic share: ${quadraticShare.toString()}%`);
  // }

  const projectShares = await dao.getProjectShares();
  console.log(`Project shares: ${projectShares.toString()}`);

  const projectSharesAsPerQuadraticVoting = await dao.getProjectSharesQuadratic();
  console.log(`Project shares as per quadratic voting: ${projectSharesAsPerQuadraticVoting.toString()}`);

  const investorsInfo = await dao.getInvestorsInfo();
  console.log(`Investors info: ${investorsInfo.toString()}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
