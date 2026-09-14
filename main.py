import os
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import InvalidToken
from etape5_login import LoginWindow
from etape6_main_window import MainWindow
from etape3_storage import load_vault, save_vault, VAULT_FILE


def apply_style():
    style = ttk.Style()
    style.theme_use("clam")

    bg_color = "#fdf6e3"
    accent_color = "#77955f"
    accent_dark = "#5f7a4d"
    text_color = "#3a3a3a"

    style.configure("TButton", padding=8, font=("Segoe UI", 10), background=accent_color, foreground="white")
    style.map("TButton", background=[("active", accent_dark)])

    style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
    style.configure("TEntry", padding=5, font=("Segoe UI", 10))
    style.configure("TFrame", background=bg_color)


if __name__ == "__main__":
    login_root = tk.Tk()
    login_root.configure(bg="#fdf6e3")
    apply_style()

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
    main_root.configure(bg="#fdf6e3")
    apply_style()

    main_app = MainWindow(main_root, master_key, data)
    main_root.mainloop()