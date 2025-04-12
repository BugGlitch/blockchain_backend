# blockchain/utils.py
import json, hashlib
from ecdsa import SigningKey, SECP256k1

def sign_transaction(tx_data, private_key_hex):
    sk = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    tx_string = json.dumps(tx_data, sort_keys=True)
    signature = sk.sign(tx_string.encode())
    return signature.hex()


def is_valid_address(address):
    if not isinstance(address, str) or len(address) != 64:
        return False
    try:
        int(address, 16)
        return True
    except ValueError:
        return False
