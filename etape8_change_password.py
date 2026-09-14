import tkinter as tk
from tkinter import messagebox
from etape1_cle import generate_salt, derive_key
from etape3_storage import save_vault
from etape5_login import hash_password, load_config, save_config


class ChangePasswordWindow:
    def __init__(self, parent, current_master_key, data):
        self.current_master_key = current_master_key
        self.data = data
        self.new_master_key = None

        self.window = tk.Toplevel(parent)
        self.window.title("Change master password")

        tk.Label(self.window, text="Current password:").grid(row=0, column=0, sticky="e")
        self.current_entry = tk.Entry(self.window, show="*")
        self.current_entry.grid(row=0, column=1)
        tk.Button(self.window, text="👁", command=lambda: self.toggle_visibility(self.current_entry)).grid(row=0, column=2)

        tk.Label(self.window, text="New password:").grid(row=1, column=0, sticky="e")
        self.new_entry = tk.Entry(self.window, show="*")
        self.new_entry.grid(row=1, column=1)
        tk.Button(self.window, text="👁", command=lambda: self.toggle_visibility(self.new_entry)).grid(row=1, column=2)

        tk.Label(self.window, text="Confirm new password:").grid(row=2, column=0, sticky="e")
        self.confirm_entry = tk.Entry(self.window, show="*")
        self.confirm_entry.grid(row=2, column=1)
        tk.Button(self.window, text="👁", command=lambda: self.toggle_visibility(self.confirm_entry)).grid(row=2, column=2)

        tk.Button(self.window, text="Change", command=self.on_change).grid(row=3, column=0, columnspan=3, pady=10)

    def toggle_visibility(self, entry_widget):
        if entry_widget.cget("show") == "*":
            entry_widget.config(show="")
        else:
            entry_widget.config(show="*")

    def on_change(self):
        current_password = self.current_entry.get()
        new_password = self.new_entry.get()
        confirm_password = self.confirm_entry.get()

        config = load_config()
        current_hash = hash_password(current_password, config["salt"])

        if current_hash != config["password_hash"]:
            messagebox.showerror("Error", "Current password is incorrect.")
            return

        if not new_password:
            messagebox.showerror("Error", "New password cannot be empty.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New password and confirmation do not match.")
            return

        new_salt = generate_salt()
        new_hash = hash_password(new_password, new_salt)
        save_config(new_salt, new_hash)

        self.new_master_key = derive_key(new_password, new_salt)
        save_vault(self.new_master_key, self.data)

        messagebox.showinfo("Success", "Master password changed successfully.")
        self.window.destroy()