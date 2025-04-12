# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from blockchain.wallet import create_wallet
# from blockchain.transaction import sign_transaction
# from blockchain.chain import Blockchain
# from blockchain.utils import is_valid_address

# app = Flask(__name__)
# CORS(app)

# blockchain = Blockchain()

# # In-memory user db
# users_db = {}

# # Known wallets (simulate valid ones)
# known_wallets = [
#     "353b5c66a0713f77d1c77507333338985dc836ac6087902411ccf1cf151efc14",
#     "302e6adb8e156e333d2abb54ba592e30b55ffdc0be6d0e38dcc1651d84b47a5a",
#     "27c948f4cbdba80dfab99a47e36e4ea84b98cbfa56a62417d824f6cde44a21d2"
# ]

# @app.route('/wallet/new', methods=['GET'])
# def new_wallet():
#     wallet = create_wallet()
#     known_wallets.append(wallet['address'])
#     return jsonify(wallet), 200

# @app.route('/transaction/new', methods=['POST'])
# def new_transaction():
#     tx_data = request.get_json()

#     required = ['sender', 'receiver', 'amount', 'public_key', 'private_key']
#     if not all(k in tx_data for k in required):
#         return jsonify({"success": False, "message": "Missing fields"}), 400

#     if not is_valid_address(tx_data["receiver"]):
#         return jsonify({"success": False, "message": "Invalid receiver address format"}), 400

#     if tx_data["receiver"] not in known_wallets:
#         return jsonify({"success": False, "message": "Receiver not found"}), 404

#     signature = sign_transaction({
#         "sender": tx_data["sender"],
#         "receiver": tx_data["receiver"],
#         "amount": tx_data["amount"]
#     }, tx_data["private_key"])

#     transaction = {
#         "sender": tx_data["sender"],
#         "receiver": tx_data["receiver"],
#         "amount": tx_data["amount"],
#         "public_key": tx_data["public_key"],
#         "signature": signature
#     }

#     success = blockchain.add_transaction(transaction)
#     return jsonify({"success": success, "message": "Transaction added" if success else "Transaction invalid"})

# @app.route('/mine', methods=['GET'])
# def mine_block():
#     index = blockchain.mine()
#     return jsonify({"block_index": index}), 200

# @app.route('/chain', methods=['GET'])
# def get_chain():
#     chain_data = []
#     for block in blockchain.chain:
#         chain_data.append({
#             "index": block.index,
#             "hash": block.hash,
#             "previous_hash": block.previous_hash,
#             "transactions": block.transactions
#         })
#     return jsonify(chain_data), 200

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')
#     wallet_address = data.get('walletAddress')

#     print(f"Received data: {data}")  # Print to check the received data

#     if not all([email, password, wallet_address]):
#         return jsonify({"success": False, "message": "All fields required"}), 400

#     if wallet_address not in known_wallets:
#         return jsonify({"success": False, "message": "Invalid wallet address"}), 400

#     if email in users_db:
#         return jsonify({"success": False, "message": "User already exists"}), 409

#     users_db[email] = {
#         "password": password,
#         "wallet": wallet_address
#     }
#     return jsonify({"success": True, "message": "User registered"}), 201


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not all([email, password]):
#         return jsonify({"success": False, "message": "Missing credentials"}), 400

#     user = users_db.get(email)
#     if not user or user["password"] != password:
#         return jsonify({"success": False, "message": "Invalid credentials"}), 401

#     return jsonify({"success": True, "message": "Login successful", "wallet": user["wallet"]}), 200

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from blockchain.wallet import create_wallet
from blockchain.transaction import sign_transaction, is_valid_hex
from blockchain.chain import Blockchain
from blockchain.utils import is_valid_address

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()
users_db = {}

# Known wallets (simulate valid ones)
known_wallets = [
    "353b5c66a0713f77d1c77507333338985dc836ac6087902411ccf1cf151efc14",
    "302e6adb8e156e333d2abb54ba592e30b55ffdc0be6d0e38dcc1651d84b47a5a",
    "27c948f4cbdba80dfab99a47e36e4ea84b98cbfa56a62417d824f6cde44a21d2"
]

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    wallet = create_wallet()
    if wallet['address'] not in known_wallets:
        known_wallets.append(wallet['address'])
    return jsonify(wallet), 200

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    
    # Log the incoming data for debugging
    print("Incoming Data:", tx_data)  # This will print the payload from the frontend

    required = ['sender', 'receiver', 'amount', 'public_key', 'private_key']
    if not all(k in tx_data for k in required):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    # Validate receiver address format (Assuming is_valid_address function is defined)
    if not is_valid_address(tx_data["receiver"]):
        return jsonify({"success": False, "message": "Invalid receiver address format"}), 400

    # Validate if the receiver exists in known wallets (Assuming known_wallets is defined)
    if tx_data["receiver"] not in known_wallets:
        return jsonify({"success": False, "message": "Receiver not found"}), 404

    try:
        # Ensure private_key is a string and is in hexadecimal format
        private_key = tx_data["private_key"]
        if not isinstance(private_key, str):
            raise ValueError("Private key must be a string")

        if not is_valid_hex(private_key):
            raise ValueError("Private key must be a valid hex string")

        # Signing the transaction
        transaction_data = {
            "sender": tx_data["sender"],
            "receiver": tx_data["receiver"],
            "amount": tx_data["amount"]
        }
        signature = sign_transaction(private_key, transaction_data)

    except Exception as e:
        # Catch any errors that occur during signing and log them
        print(f"Error during transaction signing: {str(e)}")
        return jsonify({"success": False, "message": f"Signing failed: {str(e)}"}), 500

    # Continue with the rest of the transaction processing
    transaction = {
        "sender": tx_data["sender"],
        "receiver": tx_data["receiver"],
        "amount": tx_data["amount"],
        "public_key": tx_data["public_key"],
        "signature": signature
    }

    # Add the transaction to the blockchain (Assuming blockchain.add_transaction is defined)
    success = blockchain.add_transaction(transaction)
    return jsonify({"success": success, "message": "Transaction added" if success else "Transaction invalid"})

@app.route('/mine', methods=['GET'])
def mine_block():
    index = blockchain.mine()
    if index is None:
        return jsonify({"success": False, "message": "No transactions to mine"}), 400
    return jsonify({"success": True, "message": "Block mined", "block_index": index}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify([
        {
            "index": block.index,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "transactions": block.transactions
        }
        for block in blockchain.chain
    ]), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    wallet_address = data.get('walletAddress')

    if not all([email, password, wallet_address]):
        return jsonify({"success": False, "message": "All fields required"}), 400

    if wallet_address not in known_wallets:
        return jsonify({"success": False, "message": "Invalid wallet address"}), 400

    if email in users_db:
        return jsonify({"success": False, "message": "User already exists"}), 409

    users_db[email] = {
        "password": password,
        "wallet": wallet_address
    }
    return jsonify({"success": True, "message": "User registered"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_db.get(email)
    if not user or user["password"] != password:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    return jsonify({"success": True, "message": "Login successful", "wallet": user["wallet"]}), 200

if __name__ == '__main__':
    app.run(debug=True)
