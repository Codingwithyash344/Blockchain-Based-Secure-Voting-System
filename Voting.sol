// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    struct Voter {
        bool registered;
        bool voted;
        uint vote;  // Candidate index
    }

    struct Candidate {
        string name;
        uint voteCount;
    }

    address public admin;
    mapping(address => Voter) public voters;
    Candidate[] public candidates;

    event VoterRegistered(address voter);
    event VoteCast(address voter, uint candidate);

    constructor(string[] memory candidateNames) {
        admin = msg.sender;
        for (uint i = 0; i < candidateNames.length; i++) {
            candidates.push(Candidate(candidateNames[i], 0));
        }
    }

    function registerVoter(address voter) public {
        require(msg.sender == admin, "Only admin can register");
        require(!voters[voter].registered, "Already registered");
        voters[voter].registered = true;
        emit VoterRegistered(voter);
    }

    function vote(uint candidateIndex) public {
        require(voters[msg.sender].registered, "Not registered");
        require(!voters[msg.sender].voted, "Already voted");
        require(candidateIndex < candidates.length, "Invalid candidate");

        voters[msg.sender].voted = true;
        voters[msg.sender].vote = candidateIndex;
        candidates[candidateIndex].voteCount += 1;
        emit VoteCast(msg.sender, candidateIndex);
    }

    function getResults() public view returns (string[] memory, uint[] memory) {
        string[] memory names = new string[](candidates.length);
        uint[] memory counts = new uint[](candidates.length);
        for (uint i = 0; i < candidates.length; i++) {
            names[i] = candidates[i].name;
            counts[i] = candidates[i].voteCount;
        }
        return (names, counts);
    }
}
