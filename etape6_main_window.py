import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from etape3_storage import save_vault, load_vault
from etape4_vault_logic import add_entry, update_entry, delete_entry, generate_password, MAX_CUSTOM_FIELDS
from etape8_change_password import ChangePasswordWindow

class MainWindow:
    def __init__(self, root, master_key, data):
        self.root = root
        self.master_key = master_key
        self.data = data

        self.root.title("My Password Vault")

        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack(padx=10, pady=10)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Add", command=self.open_add_form).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Edit", command=self.open_edit_form).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_selected).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Show/Copy", command=self.show_selected).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Change Password", command=self.open_change_password).grid(row=0, column=4, padx=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for entry in self.data["entries"]:
            self.listbox.insert(tk.END, f"{entry['category']} | {entry['name']}")

    def get_selected_index(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select an entry first.")
            return None
        return selection[0]

    def save_and_refresh(self):
        save_vault(self.master_key, self.data)
        self.refresh_list()

    def delete_selected(self):
        index = self.get_selected_index()
        if index is None:
            return
        delete_entry(self.data, index)
        self.save_and_refresh()

    def show_selected(self):
        index = self.get_selected_index()
        if index is None:
            return
        entry = self.data["entries"][index]

        details = f"Name: {entry['name']}\nCategory: {entry['category']}\nPassword: {entry['password']}"
        for field_name, field_value in entry["custom_fields"].items():
            details += f"\n{field_name}: {field_value}"

        self.root.clipboard_clear()
        self.root.clipboard_append(entry["password"])
        messagebox.showinfo("Entry details (password copied)", details)

    def open_add_form(self):
        EntryForm(self.root, self, mode="add")

    def open_edit_form(self):
        index = self.get_selected_index()
        if index is None:
            return
        EntryForm(self.root, self, mode="edit", index=index)
    
    def open_change_password(self):
        dialog = ChangePasswordWindow(self.root, self.master_key, self.data)
        self.root.wait_window(dialog.window)
        if dialog.new_master_key:
            self.master_key = dialog.new_master_key


class EntryForm:
    def __init__(self, parent, main_window, mode, index=None):
        self.main_window = main_window
        self.mode = mode
        self.index = index
        self.custom_field_rows = []

        self.window = tk.Toplevel(parent)
        self.window.title("Add entry" if mode == "add" else "Edit entry")

        ttk.Label(self.window, text="Category:").grid(row=0, column=0, sticky="e")
        self.category_entry = ttk.Entry(self.window)
        self.category_entry.grid(row=0, column=1)

        ttk.Label(self.window, text="Name:").grid(row=1, column=0, sticky="e")
        self.name_entry = ttk.Entry(self.window)
        self.name_entry.grid(row=1, column=1)

        ttk.Label(self.window, text="Password:").grid(row=2, column=0, sticky="e")
        self.password_entry = ttk.Entry(self.window)
        self.password_entry.grid(row=2, column=1)
        ttk.Button(self.window, text="Generate", command=self.fill_generated_password).grid(row=2, column=2)

        self.custom_fields_frame = ttk.Frame(self.window)
        self.custom_fields_frame.grid(row=3, column=0, columnspan=3, pady=5)

        self.add_field_button = ttk.Button(self.window, text="+ Add custom field", command=self.add_custom_field_row)
        self.add_field_button.grid(row=4, column=0, columnspan=3)

        ttk.Button(self.window, text="Save", command=self.save).grid(row=5, column=0, columnspan=3, pady=10)

        if mode == "edit":
            self.load_existing_data()

    def fill_generated_password(self):
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, generate_password())

    def add_custom_field_row(self):
        if len(self.custom_field_rows) >= MAX_CUSTOM_FIELDS:
            messagebox.showwarning("Limit reached", f"Maximum {MAX_CUSTOM_FIELDS} custom fields.")
            return

        row_frame = ttk.Frame(self.custom_fields_frame)
        row_frame.pack(pady=2)

        field_name_entry = ttk.Entry(row_frame, width=15)
        field_name_entry.pack(side="left", padx=2)

        field_value_entry = ttk.Entry(row_frame, width=20)
        field_value_entry.pack(side="left", padx=2)

        remove_button = ttk.Button(row_frame, text="x", command=lambda: self.remove_custom_field_row(row_frame))
        remove_button.pack(side="left", padx=2)

        self.custom_field_rows.append((row_frame, field_name_entry, field_value_entry))

        if len(self.custom_field_rows) >= MAX_CUSTOM_FIELDS:
            self.add_field_button.config(state="disabled")

    def remove_custom_field_row(self, row_frame):
        self.custom_field_rows = [
            row for row in self.custom_field_rows if row[0] != row_frame
        ]
        row_frame.destroy()
        self.add_field_button.config(state="normal")

    def load_existing_data(self):
        entry = self.main_window.data["entries"][self.index]
        self.category_entry.insert(0, entry["category"])
        self.name_entry.insert(0, entry["name"])
        self.password_entry.insert(0, entry["password"])

        for field_name, field_value in entry["custom_fields"].items():
            self.add_custom_field_row()
            _, name_entry, value_entry = self.custom_field_rows[-1]
            name_entry.insert(0, field_name)
            value_entry.insert(0, field_value)

    def collect_custom_fields(self) -> dict:
        custom_fields = {}
        for _, field_name_entry, field_value_entry in self.custom_field_rows:
            field_name = field_name_entry.get().strip()
            field_value = field_value_entry.get().strip()
            if field_name:
                custom_fields[field_name] = field_value
        return custom_fields

    def save(self):
        category = self.category_entry.get().strip()
        name = self.name_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not password:
            messagebox.showerror("Error", "Name and password are required.")
            return

        custom_fields = self.collect_custom_fields()

        if self.mode == "add":
            add_entry(self.main_window.data, category, name, password, custom_fields)
        else:
            update_entry(self.main_window.data, self.index, category, name, password, custom_fields)

        self.main_window.save_and_refresh()
        self.window.destroy()
        
        
if __name__ == "__main__":
    from etape1_cle import generate_salt, derive_key

    salt = generate_salt()
    key = derive_key("test1234", salt)
    data = {"entries": []}

    root = tk.Tk()
    app = MainWindow(root, key, data)
    root.mainloop()