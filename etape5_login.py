import os
import json
import hashlib
import tkinter as tk
from tkinter import messagebox
from etape1_cle import generate_salt, derive_key

CONFIG_FILE = "config.json"


def hash_password(password: str, salt: bytes) -> str:
    return hashlib.sha256(salt + password.encode()).hexdigest()


def config_exists() -> bool:
    return os.path.exists(CONFIG_FILE)


def save_config(salt: bytes, password_hash: str):
    config = {
        "salt": salt.hex(),
        "password_hash": password_hash,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def load_config() -> dict:
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    config["salt"] = bytes.fromhex(config["salt"])
    return config


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Vault")
        self.master_key = None

        self.label = tk.Label(root, text="")
        self.label.pack(pady=10)

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.button = tk.Button(root, text="", command=self.on_submit)
        self.button.pack(pady=10)

        if config_exists():
            self.mode = "login"
            self.label.config(text="Enter your master password:")
            self.button.config(text="Login")
        else:
            self.mode = "create"
            self.label.config(text="Create a master password:")
            self.button.config(text="Create")

    def on_submit(self):
        password = self.password_entry.get()

        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        if self.mode == "create":
            salt = generate_salt()
            password_hash = hash_password(password, salt)
            save_config(salt, password_hash)
            self.master_key = derive_key(password, salt)
            messagebox.showinfo("Success", "Master password created!")
            self.root.destroy()
        else:
            config = load_config()
            entered_hash = hash_password(password, config["salt"])
            if entered_hash == config["password_hash"]:
                self.master_key = derive_key(password, config["salt"])
                messagebox.showinfo("Success", "Login successful!")
                self.root.destroy()
            else:
                messagebox.showerror("Error", "Wrong password.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

    if app.master_key:
        print("Master key ready to use:", app.master_key)