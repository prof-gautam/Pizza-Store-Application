import tkinter as tk
from tkinter import ttk, messagebox
from business_logic import MenuManager  # Assuming MenuManager exists in business_logic

class MenuUI:
    def __init__(self, master):
        self.master = master
        self.menu_manager = MenuManager()
        self.setup_ui()

    def setup_ui(self):
        # self.master.title("Menu Management")

        # Labels and Entry fields for menu item details
        ttk.Label(self.master, text="Name:").grid(row=0, column=0, padx=10, pady=2)
        self.name_entry = ttk.Entry(self.master, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=2)

        ttk.Label(self.master, text="Description:").grid(row=1, column=0, padx=10, pady=2)
        self.description_entry = ttk.Entry(self.master, width=30)
        self.description_entry.grid(row=1, column=1, padx=10, pady=2)

        ttk.Label(self.master, text="Price:").grid(row=2, column=0, padx=10, pady=2)
        self.price_entry = ttk.Entry(self.master, width=30)
        self.price_entry.grid(row=2, column=1, padx=10, pady=2)

        # Buttons for adding, editing, and deleting menu items
        add_button = ttk.Button(self.master, text="Add Item", command=self.add_item)
        add_button.grid(row=3, column=0, padx=10, pady=10)

        edit_button = ttk.Button(self.master, text="Edit Item", command=self.edit_item)
        edit_button.grid(row=3, column=1, padx=10, pady=10)

        delete_button = ttk.Button(self.master, text="Delete Item", command=self.delete_item)
        delete_button.grid(row=3, column=2, padx=10, pady=10)

        # Table for displaying menu items
        self.menu_table = ttk.Treeview(self.master, columns=("Name", "Description", "Price"), show='headings')
        self.menu_table.heading("Name", text="Name")
        self.menu_table.heading("Description", text="Description")
        self.menu_table.heading("Price", text="Price")
        self.menu_table.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky='nsew')

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure(4, weight=1)

        # Display menu items
        self.display_menu_items()

    def display_menu_items(self):
        for item in self.menu_table.get_children():
            self.menu_table.delete(item)
        for item in self.menu_manager.get_menu_items():
            self.menu_table.insert('', 'end', values=(item.name, item.description, item.price))

    def add_item(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        price_str = self.price_entry.get()

        if not name or not description or not price_str:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            price = float(price_str)
            if price < 0:
                raise ValueError("Price must be positive.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid price format: {e}")
            return

        self.menu_manager.add_menu_item(name, description, price)  # Assuming this method exists in MenuManager
        self.display_menu_items()

        # Clear the input fields
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


    def edit_item(self):
        selected_item = self.menu_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No menu item selected")
            return

        name = self.name_entry.get()
        description = self.description_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid price format")
            return

        self.menu_manager.update_menu_item(selected_item[0], name, description, price)
        self.display_menu_items()

    def delete_item(self):
        selected_item = self.menu_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No menu item selected")
            return

        self.menu_manager.delete_menu_item(selected_item[0])
        self.display_menu_items()

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = MenuUI(root)
    root.mainloop()
