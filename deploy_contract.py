from web3 import Web3
import json
import os
from solcx import compile_standard

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
if not w3.is_connected():
    raise Exception("Cannot connect to Ganache")

# Load Solidity source
with open('Voting.sol', 'r') as file:
    source = file.read()

# Compile
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"Voting.sol": {"content": source}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}}
}, solc_version="0.8.0")

# Extract bytecode and ABI
bytecode = compiled_sol['contracts']['Voting.sol']['Voting']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['Voting.sol']['Voting']['abi']

# Deploy
account = w3.eth.accounts[0]  # Use first Ganache account
Voting = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Voting.constructor(["Alice", "Bob", "Charlie"]).transact({'from': account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

# Save ABI and address for later use
with open('contract_abi.json', 'w') as f:
    json.dump(abi, f)
with open('contract_address.txt', 'w') as f:
    f.write(contract_address)

print(f"Contract deployed at: {contract_address}")
