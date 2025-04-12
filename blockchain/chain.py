from .block import Block
from .transaction import verify_transaction

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        # Validate transaction before adding
        tx_data = {
            "sender": transaction["sender"],
            "receiver": transaction["receiver"],
            "amount": transaction["amount"]
        }
        if verify_transaction(transaction["public_key"], tx_data, transaction["signature"]):
            self.unconfirmed_transactions.append(transaction)
            return True
        return False

    def proof_of_work(self, block, difficulty=2):
        while not block.hash.startswith('0' * difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()
        return block.hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not proof.startswith('0' * 2):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        new_block = Block(len(self.chain), self.unconfirmed_transactions, self.last_block.hash)
        proof = self.proof_of_work(new_block)
        success = self.add_block(new_block, proof)
        if success:
            self.unconfirmed_transactions = []
            return new_block.index
        return False
