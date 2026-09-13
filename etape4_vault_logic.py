import secrets
import string
from etape1_cle import generate_salt, derive_key
from etape3_storage import save_vault, load_vault

MAX_CUSTOM_FIELDS = 5


def add_entry(data: dict, category: str, name: str, password: str, custom_fields: dict = None):
    if custom_fields is None:
        custom_fields = {}

    if len(custom_fields) > MAX_CUSTOM_FIELDS:
        raise ValueError(f"Too many custom fields (max {MAX_CUSTOM_FIELDS})")

    data["entries"].append({
        "category": category,
        "name": name,
        "password": password,
        "custom_fields": custom_fields,
    })


def update_entry(data: dict, index: int, category: str, name: str, password: str, custom_fields: dict = None):
    if custom_fields is None:
        custom_fields = {}

    if len(custom_fields) > MAX_CUSTOM_FIELDS:
        raise ValueError(f"Too many custom fields (max {MAX_CUSTOM_FIELDS})")

    data["entries"][index] = {
        "category": category,
        "name": name,
        "password": password,
        "custom_fields": custom_fields,
    }


def delete_entry(data: dict, index: int):
    del data["entries"][index]


def list_entries(data: dict):
    for i, entry in enumerate(data["entries"]):
        print(f"[{i}] {entry['category']} | {entry['name']} | {entry['password']}")
        for field_name, field_value in entry["custom_fields"].items():
            print(f"      - {field_name}: {field_value}")


def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


if __name__ == "__main__":
    salt = generate_salt()
    master_password = "test1234"
    key = derive_key(master_password, salt)

    data = {"entries": []}

    add_entry(data, "Streaming", "Netflix", "azerty123")

    add_entry(
        data,
        "Banque",
        "BNP",
        "monmdp123",
        custom_fields={
            "Numéro de compte": "FR76 1234 5678",
            "Code PIN": "1234",
        },
    )

    print("--- List after adding 2 entries ---")
    list_entries(data)

    save_vault(key, data)
    print("\nVault saved.")