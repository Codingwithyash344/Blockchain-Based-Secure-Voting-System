from solcx import compile_standard, install_solc
import json

# Install the Solidity compiler version you need
install_solc("0.8.17")

# Load your Solidity source code
with open("Voting.sol", "r") as file:
    source_code = file.read()

# Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"Voting.sol": {"content": source_code}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "evm.bytecode"]}
        }
    }
})

# Extract and save the ABI
abi = compiled_sol["contracts"]["Voting.sol"]["Voting"]["abi"]
with open("contract_abi.json", "w") as f:
    json.dump(abi, f)
