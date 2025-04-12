from blockchain.wallet import create_wallet
from blockchain.transaction import sign_transaction, create_transaction
from blockchain.chain import Blockchain

# Step 1: Create wallets
sender = create_wallet()
receiver = create_wallet()

# Step 2: Create blockchain
chain = Blockchain()

# Step 3: Create transaction data
tx_data = {
    "sender": sender["address"],
    "receiver": receiver["address"],
    "amount": 100
}

# Step 4: Sign the transaction
signature = sign_transaction(sender["private_key"], tx_data)

# Step 5: Create full transaction
transaction = create_transaction(
    sender["address"],
    receiver["address"],
    100,
    sender["public_key"],
    signature
)

# Step 6: Add transaction to blockchain
added = chain.add_transaction(transaction)
print("Transaction added?", added)

# Step 7: Mine the block
mined_index = chain.mine()
print("Mined Block Index:", mined_index)

# Step 8: Print full blockchain
print("\nBlockchain:")
for block in chain.chain:
    print(f"\nBlock #{block.index}")
    print("Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
    print("Transactions:", block.transactions)
