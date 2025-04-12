# # import json
# # from ecdsa import SigningKey, SECP256k1

# # # Function to check if a string is a valid hex string
# # def is_valid_hex(s):
# #     try:
# #         bytes.fromhex(s)
# #         return True
# #     except ValueError:
# #         return False

# # # Sign the transaction
# # def sign_transaction(private_key_hex, transaction_data):
# #     # Validate the private key hex string
# #     if not is_valid_hex(private_key_hex):
# #         raise ValueError("Invalid private key hex format.")
    
# #     try:
# #         # Convert private key from hex to bytes and sign the transaction
# #         private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
# #         message = json.dumps(transaction_data, sort_keys=True).encode()
# #         signature = private_key.sign(message)
# #         return signature.hex()
# #     except Exception as e:
# #         raise ValueError(f"Signing failed: {str(e)}")


# # import json
# # from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError

# # def sign_transaction(private_key_hex, transaction_data):
# #     private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
# #     message = json.dumps(transaction_data, sort_keys=True).encode()
# #     signature = private_key.sign(message)
# #     return signature.hex()

# # def verify_transaction(public_key_hex, transaction_data, signature_hex):
# #     public_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
# #     message = json.dumps(transaction_data, sort_keys=True).encode()
# #     try:
# #         return public_key.verify(bytes.fromhex(signature_hex), message)
# #     except BadSignatureError:
# #         return False


# import hashlib
# from ecdsa import SECP256k1, VerifyingKey

# # Function to sign a transaction
# def sign_transaction(private_key, transaction_data):
#     # Here, use your preferred signing method, like elliptic curve signing (ECDSA) or RSA
#     # This is a placeholder for signing the transaction with the private key
#     # In practice, this would sign the transaction with the private key and return the signature

#     # Let's assume the private key is a string, for simplicity
#     message = f"{transaction_data['sender']}{transaction_data['receiver']}{transaction_data['amount']}"
#     # You can sign using a real private key and cryptographic library, but here's a mock example
#     signed_message = hashlib.sha256(message.encode('utf-8')).hexdigest()
#     return signed_message

# # Function to verify a transaction
# def verify_transaction(public_key, transaction_data, signature):
#     # Use the public key to verify the transaction signature
#     # This example assumes we are using ECDSA and verifying with the public key
#     # In practice, you'd use the ECDSA library or a similar library for real-world apps
#     try:
#         # Convert public key to verifying key
#         vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)

#         # Verify the signature matches the data
#         message = f"{transaction_data['sender']}{transaction_data['receiver']}{transaction_data['amount']}"
#         return vk.verify(bytes.fromhex(signature), message.encode('utf-8'))
#     except Exception as e:
#         print(f"Error verifying transaction: {e}")
#         return False

# # Helper function to check if a string is valid hex
# def is_valid_hex(value):
#     return all(c in '0123456789abcdefABCDEF' for c in value)

import json
import binascii
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

def is_valid_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def sign_transaction(private_key_hex, transaction_data):
    private_key_bytes = binascii.unhexlify(private_key_hex)
    private_key = ec.derive_private_key(int.from_bytes(private_key_bytes, 'big'), ec.SECP256K1())
    data_string = json.dumps(transaction_data, sort_keys=True).encode()
    signature = private_key.sign(data_string, ec.ECDSA(hashes.SHA256()))
    return binascii.hexlify(signature).decode()

def verify_transaction(public_key_hex, transaction_data, signature_hex):
    try:
        # Prepend '04' for uncompressed public key format
        public_key_hex = "04" + public_key_hex

        public_key_bytes = binascii.unhexlify(public_key_hex)
        signature_bytes = binascii.unhexlify(signature_hex)

        public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), public_key_bytes)
        data_string = json.dumps(transaction_data, sort_keys=True).encode()

        public_key.verify(signature_bytes, data_string, ec.ECDSA(hashes.SHA256()))
        return True
    except (ValueError, InvalidSignature, binascii.Error) as e:
        print("Verification failed:", str(e))
        return False
