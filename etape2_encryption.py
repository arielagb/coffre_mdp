from cryptography.fernet import Fernet
from etape1_cle import generate_salt, derive_key


def encrypt_text(key: bytes, plain_text: str) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(plain_text.encode())


def decrypt_text(key: bytes, encrypted_text: bytes) -> str:
    fernet = Fernet(key)
    decrypted_bytes = fernet.decrypt(encrypted_text)
    return decrypted_bytes.decode()


if __name__ == "__main__":
    salt = generate_salt()
    master_password = "test1234"
    key = derive_key(master_password, salt)

    message = "This is my Netflix password: azerty123"
    print("Original message:", message)

    encrypted = encrypt_text(key, message)
    print("Encrypted:", encrypted)

    decrypted = decrypt_text(key, encrypted)
    print("Decrypted:", decrypted)

    print("Does it match the original?", message == decrypted)