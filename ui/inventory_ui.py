import tkinter as tk
from tkinter import ttk, messagebox
from business_logic import InventoryManager

class InventoryUI:
    def __init__(self, master):
        self.master = master
        self.inventory_manager = InventoryManager()
        self.setup_ui()

    def setup_ui(self):
        # Configure the grid weight for scaling
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Entry fields for inventory item name and quantity
        ttk.Label(self.master, text="Item Name:").grid(row=0, column=0, padx=10, pady=2, sticky='w')
        self.item_name_entry = ttk.Entry(self.master)
        self.item_name_entry.grid(row=0, column=1, padx=10, pady=2, sticky='ew')  # Expanded horizontally

        ttk.Label(self.master, text="Quantity:").grid(row=1, column=0, padx=10, pady=2, sticky='w')
        self.quantity_entry = ttk.Entry(self.master)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=2, sticky='ew')  # Expanded horizontally

        # Buttons for adding, updating, and deleting inventory items
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky='ew')
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Equal weight to all buttons

        add_button = ttk.Button(button_frame, text="Add Item", command=self.add_item)
        add_button.grid(row=0, column=0, padx=5, pady=2, sticky='ew')

        update_button = ttk.Button(button_frame, text="Update Item", command=self.update_item)
        update_button.grid(row=0, column=1, padx=5, pady=2, sticky='ew')

        delete_button = ttk.Button(button_frame, text="Delete Item", command=self.delete_item)
        delete_button.grid(row=0, column=2, padx=5, pady=2, sticky='ew')

        check_stock_button = ttk.Button(button_frame, text="Check Low Stock", command=self.check_low_stock)
        check_stock_button.grid(row=0, column=3, padx=5, pady=2, sticky='ew')

        # Table for displaying inventory items
        self.inventory_table = ttk.Treeview(self.master, columns=("Item Name", "Quantity"), show='headings')
        self.inventory_table.heading("Item Name", text="Item Name")
        self.inventory_table.heading("Quantity", text="Quantity")
        self.inventory_table.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky='nsew')  # Expanded in all directions

        # Scrollbar for the table
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.inventory_table.yview)
        scrollbar.grid(row=3, column=2, sticky='ns')
        self.inventory_table.configure(yscrollcommand=scrollbar.set)

        self.display_inventory()
    def display_inventory(self):
        for item in self.inventory_table.get_children():
            self.inventory_table.delete(item)
        for item_name, item in self.inventory_manager.inventory.items():
            self.inventory_table.insert('', 'end', values=(item_name, item.quantity))

    def add_item(self):
        item_name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()

        if not item_name or not quantity.isdigit():
            messagebox.showerror("Error", "Item name must be filled out and quantity must be a number.")
            return

        self.inventory_manager.add_item(item_name, int(quantity))
        self.display_inventory()

    def update_item(self):
        item_name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()

        if not item_name or not quantity.isdigit():
            messagebox.showerror("Error", "Item name must be filled out and quantity must be a number.")
            return

        self.inventory_manager.update_item(item_name, int(quantity))
        self.display_inventory()

    def delete_item(self):
        selected_item = self.inventory_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to delete.")
            return

        item_name = self.inventory_table.item(selected_item, 'values')[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?")
        if confirm:
            self.inventory_manager.delete_item(item_name)
            self.display_inventory()
    
    def check_low_stock(self):
        low_stock_items = self.inventory_manager.get_low_stock_items(threshold=10)  # Adjust threshold as needed
        if low_stock_items:
            message = "Low stock for items:\n" + "\n".join([f"{item.name}: {item.quantity}" for item in low_stock_items])
            messagebox.showwarning("Low Stock Alert", message)
        else:
            messagebox.showinfo("Stock Check", "All items are sufficiently stocked.")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = InventoryUI(root)
    root.mainloop()
