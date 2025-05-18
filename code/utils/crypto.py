import base64
import rsa

# from cryptography.hazmat.primitives.asymmetric import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA1
import base64
import math


def encrypt_rsa(text: str, public_key_pem: str) -> str:
    # Load the public key from the PEM-encoded string
    key = RSA.importKey(public_key_pem)
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA1)

    key_size = key.size_in_bytes()
    max_chunk_size = key_size - 2 * SHA1.digest_size - 2

    chunks = [
        cipher.encrypt(text[i:i+max_chunk_size].encode())
        for i in range(0, len(text), max_chunk_size)
    ]

    encrypted = b''.join(chunks)
    return base64.b64encode(encrypted).decode()

    # Return base64 encoded result


def md5(text: str) -> str:
    """
    Calculates the MD5 hash of the provided text.

    Args:
        text: Input string to hash

    Returns:
        Hexadecimal string representation of the MD5 hash
    """
    import hashlib
    return hashlib.md5(text.encode('utf-8')).hexdigest()
