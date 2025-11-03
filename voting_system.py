from web3 import Web3
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load contract
with open('contract_abi.json', 'r') as f:
    abi = json.load(f)
with open('contract_address.txt', 'r') as f:
    contract_address = f.read().strip()

contract = w3.eth.contract(address=contract_address, abi=abi)
admin_account = w3.eth.accounts[0]

# Helper: Generate voter ID (hashed for anonymity)
def generate_voter_id(name):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(name.encode())
    return digest.finalize().hex()

# Register voter (admin only)
def register_voter(voter_address):
    tx = contract.functions.registerVoter(voter_address).transact({'from': admin_account})
    w3.eth.wait_for_transaction_receipt(tx)
    print(f"Voter {voter_address} registered.")

# Cast vote
def cast_vote(voter_account, candidate_index):
    tx = contract.functions.vote(candidate_index).transact({'from': voter_account})
    w3.eth.wait_for_transaction_receipt(tx)
    print("Vote cast successfully.")

# Get results
def get_results():
    names, counts = contract.functions.getResults().call()
    for i, name in enumerate(names):
        print(f"{name}: {counts[i]} votes")

# Main menu
def main():
    while True:
        print("\n1. Register Voter\n2. Cast Vote\n3. Get Results\n4. Exit")
        choice = input("Choose: ")
        if choice == '1':
            addr = input("Voter address: ")
            register_voter(addr)
        elif choice == '2':
            addr = input("Your address: ")
            idx = int(input("Candidate index (0-2): "))
            cast_vote(addr, idx)
        elif choice == '3':
            get_results()
        elif choice == '4':
            break

if __name__ == "__main__":
    main()
