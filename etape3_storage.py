import json
from cryptography.fernet import Fernet
from etape1_cle import generate_salt, derive_key

VAULT_FILE = "vault.enc"


def save_vault(key: bytes, data: dict):
    fernet = Fernet(key)
    json_bytes = json.dumps(data).encode()
    encrypted = fernet.encrypt(json_bytes)

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)


def load_vault(key: bytes) -> dict:
    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()

    fernet = Fernet(key)
    json_bytes = fernet.decrypt(encrypted)
    return json.loads(json_bytes)


if __name__ == "__main__":
    salt = generate_salt()
    master_password = "test1234"
    key = derive_key(master_password, salt)

    data = {
        "entries": [
            {"category": "Streaming", "name": "Netflix", "login": "ariel@mail.com", "password": "azerty123"},
            {"category": "Email", "name": "Gmail", "login": "ariel@gmail.com", "password": "mdp456"},
        ]
    }

    save_vault(key, data)
    print(f"Vault saved and encrypted in '{VAULT_FILE}'")

    loaded_data = load_vault(key)
    print("Loaded data:", loaded_data)

    print("Does it match the original?", data == loaded_data)