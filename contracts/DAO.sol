// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.17;
contract DAO {
    struct Project {
        string name;
        uint256 votes;
        string location;
        string description;
    }

    Project[] public projects;
    address[] public investors;
    mapping(address => uint256) public investments;
    mapping(address => uint256) public pendingVotes;
    
    uint256 public totalInvestment;
    uint256 public totalVotes;

    function invest() public payable {
        uint256 votes = msg.value;
        investments[msg.sender] += votes;
        pendingVotes[msg.sender] += votes;
        totalInvestment += msg.value;
        investors.push(msg.sender);
    }

    function vote(uint256 projectId, uint256 nVotes) public {
        require(nVotes <= pendingVotes[msg.sender], "Insufficient votes");
        projects[projectId].votes += nVotes;
        pendingVotes[msg.sender] -= nVotes;
        totalVotes += nVotes;
    }

    // function to cast multiple votes by a msg.sender in a single transaction
    function bulkVote(uint256[] memory projectIds, uint256[] memory nVotes) public {
        require(projectIds.length == nVotes.length, "projectIds and nVotes length mismatch");
        for (uint i = 0; i < projectIds.length; i++) {
            vote(projectIds[i], nVotes[i]);
        }
    }
    
    function getProjectShare(uint256 projectId) public view returns (uint256) {
        // if not votes, then return zero
        if (totalVotes == 0) {
            return 0;
        }
        return (projects[projectId].votes * 100) / totalVotes;
    }

    function getProjectShareAsPerQuadraticVoting(uint256 projectId) public view returns (uint256) {
        // if not votes, then return zero
        if (totalVotes == 0) {
            return 0;
        }
        uint256 quadraticVotes = projects[projectId].votes * projects[projectId].votes;
        uint256 totalQuadraticVotes = totalVotes * totalVotes;
        return (quadraticVotes * 100) / totalQuadraticVotes;
    }

    function createProject(string memory name, string memory location, string memory description) public {
       projects.push(Project(name, 0, location, description));
    }

    function getPendingVotes(address user) public view returns (uint256) {
        return pendingVotes[user];
    }

    function getInvestment(address user) public view returns (uint256) {
        return investments[user];
    }

    // New functions
    function getProjects() public view returns (string[] memory names, uint256[] memory votes, string[] memory locations, string[] memory descriptions) {
        names = new string[](projects.length);
        votes = new uint256[](projects.length);
        locations = new string[](projects.length);
        descriptions = new string[](projects.length);

        for (uint i = 0; i < projects.length; i++) {
            names[i] = projects[i].name;
            votes[i] = projects[i].votes;
            locations[i] = projects[i].location;
            descriptions[i] = projects[i].description;
        }

        return (names, votes, locations, descriptions);
    }

    function getProjectShares() public view returns (uint256[] memory shares) {
        shares = new uint256[](projects.length);

        for (uint i = 0; i < projects.length; i++) {
            shares[i] = getProjectShare(i);
        }

        return shares;
    }

    function getProjectSharesQuadratic() public view returns (uint256[] memory shares) {
        shares = new uint256[](projects.length);

        for (uint i = 0; i < projects.length; i++) {
            shares[i] = getProjectShareAsPerQuadraticVoting(i);
        }

        return shares;
    }

    function getTotalInvestment() public view returns (uint256) {
        return totalInvestment;
    }

    function getInvestorsInfo() public view returns (address[] memory _addresses, uint256[] memory _votes, uint256[] memory _investments) {
        _addresses = new address[](investors.length);
        _votes = new uint256[](investors.length);
        _investments = new uint256[](investors.length);

        for (uint i = 0; i < investors.length; i++) {
            _addresses[i] = investors[i];
            _votes[i] = pendingVotes[investors[i]];
            _investments[i] = investments[investors[i]];
        }

        return (_addresses, _votes, _investments);
    }
}
