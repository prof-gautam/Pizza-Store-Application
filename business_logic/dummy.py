import tkinter as tk
from tkinter import ttk, messagebox
from business_logic import OrderManager, MenuManager  # Assuming these classes exist

class OrderUI:
    def __init__(self, master):
        self.master = master
        self.order_manager = OrderManager()
        self.menu_manager = MenuManager()  # Assuming this class exists
        self.setup_ui()

    def setup_ui(self):
        # Styling
        style = ttk.Style()
        style.configure('TButton', foreground='black', background='white')
        style.configure('Treeview', highlightthickness=0, bd=0, font=('Helvetica', 10))
        style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))

        # Labels and Entry fields for order details
        ttk.Label(self.master, text="Order ID:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.order_id_entry = ttk.Entry(self.master, width=30)
        self.order_id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.master, text="Customer Name:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.customer_name_entry = ttk.Entry(self.master, width=30)
        self.customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Dropdown for menu items
        ttk.Label(self.master, text="Menu Item:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.menu_item_combobox = ttk.Combobox(self.master, values=[item.name for item in self.menu_manager.get_menu_items()])
        self.menu_item_combobox.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Entry for quantity
        ttk.Label(self.master, text="Quantity:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.quantity_entry = ttk.Entry(self.master, width=10)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        # Button to add item to order
        add_item_button = ttk.Button(self.master, text="Add Item to Order", command=self.add_item_to_order)
        add_item_button.grid(row=4, column=1, padx=10, pady=10, sticky='e')

        # Text box for order details (to display added items)
        ttk.Label(self.master, text="Order Details:").grid(row=5, column=0, padx=10, pady=5, sticky='nw')
        self.order_details_text = tk.Text(self.master, height=5, width=30)
        self.order_details_text.grid(row=5, column=1, padx=10, pady=5, sticky='w')

        # Buttons for managing orders
        add_button = ttk.Button(self.master, text="Add Order", command=self.add_order)
        add_button.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        update_button = ttk.Button(self.master, text="Update Order", command=self.update_order)
        update_button.grid(row=6, column=1, padx=10, pady=10, sticky='e')

        delete_button = ttk.Button(self.master, text="Delete Order", command=self.delete_order)
        delete_button.grid(row=6, column=2, padx=10, pady=10)

        # Table for displaying orders
        self.order_table = ttk.Treeview(self.master, columns=("Order ID", "Customer Name", "Details"), show='headings')
        self.order_table.heading("Order ID", text="Order ID")
        self.order_table.heading("Customer Name", text="Customer Name")
        self.order_table.heading("Details", text="Details")
        self.order_table.grid(row=7, column=0, columnspan=3, pady=10, padx=10, sticky='nsew')

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure(7, weight=1)

        # Display orders
        self.display_orders()

    def add_item_to_order(self):
        menu_item = self.menu_item_combobox.get()
        quantity = self.quantity_entry.get()
        if not menu_item or not quantity.isdigit():
            messagebox.showerror("Error", "Invalid menu item or quantity")
            return
        order_detail = f"{menu_item} x {quantity}\n"
        self.order_details_text.insert(tk.END, order_detail)


    def display_orders(self):
        for item in self.order_table.get_children():
            self.order_table.delete(item)
        for order in self.order_manager.get_orders():  # Updated method name
            self.order_table.insert('', 'end', values=(order.id, order.customer_name, order.details))

    def add_order(self):
        order_id = self.order_id_entry.get()
        customer_name = self.customer_name_entry.get()
        order_details = self.order_details_entry.get()

        # Add validation here if needed
        self.order_manager.add_order(order_id, customer_name, order_details)
        self.display_orders()

    def update_order(self):
        selected_item = self.order_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No order selected")
            return

        order_id = self.order_id_entry.get()
        new_customer_name = self.customer_name_entry.get()
        new_order_details = self.order_details_entry.get()

        # Update validation here if needed
        self.order_manager.update_order(order_id, new_customer_name, new_order_details)
        self.display_orders()

    def delete_order(self):
        selected_item = self.order_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No order selected")
            return

        order_id = self.order_table.item(selected_item, 'values')[0]
        self.order_manager.delete_order(order_id)
        self.display_orders()

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = OrderUI(root)
    root.mainloop()
