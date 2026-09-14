import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import InvalidToken
from etape5_login import LoginWindow
from etape6_main_window import MainWindow
from etape3_storage import load_vault, save_vault, VAULT_FILE

if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()

    if login_app.master_key is None:
        exit()

    master_key = login_app.master_key

    if os.path.exists(VAULT_FILE):
        try:
            data = load_vault(master_key)
        except InvalidToken:
            messagebox.showerror(
                "Error",
                "Could not decrypt the vault file. It may be corrupted."
            )
            exit()
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error while loading the vault: {e}")
            exit()
    else:
        data = {"entries": []}
        save_vault(master_key, data)

    main_root = tk.Tk()
    main_app = MainWindow(main_root, master_key, data)
    main_root.mainloop()