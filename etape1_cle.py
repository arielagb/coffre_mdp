import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def generate_salt():
    return os.urandom(16)


def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,          # Fernet requires a 32-byte key
        salt=salt,
        iterations=480_000, # slows down brute-force attacks
    )
    raw_key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(raw_key)  # Fernet requires base64


if __name__ == "__main__":
    salt = generate_salt()
    print("Generated salt (not secret, safe to store):", salt)

    master_password = "test1234"
    key = derive_key(master_password, salt)
    print("Derived key:", key)

    # Same password + same salt must always give the same key
    key_bis = derive_key(master_password, salt)
    print("Same key when recomputed?", key == key_bis)