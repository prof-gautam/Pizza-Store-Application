import tkinter as tk
import json
import subprocess
import sys
import threading
from tkinter import ttk, messagebox
from business_logic import OrderManager, MenuManager
class OrderUI:
    def __init__(self, master):
        self.master = master
        self.order_manager = OrderManager()
        self.menu_manager = MenuManager()
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
        add_button.grid(row=6, column=0, padx=5, pady=5, sticky='w')

        update_button = ttk.Button(self.master, text="Update Order", command= self.update_order)
        update_button.grid(row=6, column=1, padx=5, pady=5, sticky='e')

        delete_button = ttk.Button(self.master, text="Delete Order", command=self.delete_order)
        delete_button.grid(row=6, column=2, padx=5, pady=5)
        
        delivered_button = ttk.Button(self.master, text="Mark as Delivered", command=self.mark_as_delivered)
        delivered_button.grid(row=6, column=3, padx=5, pady=5)
        
        #print receipt
        print_receipt_button = ttk.Button(self.master, text="Print Receipt", command=self.print_receipt)
        print_receipt_button.grid(row=6, column=4, padx=5, pady=5)


        # Table for displaying orders now includes the 'Total Price' and 'Status' columns
        self.order_table = ttk.Treeview(self.master, columns=("Order ID", "Customer Name", "Details", "Status", "Total Price"), show='headings')
        # Setup headings
        self.order_table.heading("Order ID", text="Order ID")
        self.order_table.heading("Customer Name", text="Customer Name")
        self.order_table.heading("Details", text="Details")
        self.order_table.heading("Status", text="Status")
        self.order_table.heading("Total Price", text="Total Price ($)")
        # Setup column configurations
        self.order_table.column("Order ID", width=100)
        self.order_table.column("Customer Name", width=150)
        self.order_table.column("Details", width=250)
        self.order_table.column("Status", width=100)
        self.order_table.column("Total Price", width=100)
        # Grid the table
        self.order_table.grid(row=7, column=0, columnspan=5, pady=10, padx=10, sticky='nsew')

        # Display orders
        self.display_order()

    def add_item_to_order(self):
        menu_item = self.menu_item_combobox.get()
        quantity = self.quantity_entry.get()
        if not menu_item or not quantity.isdigit():
            messagebox.showerror("Error", "Invalid menu item or quantity")
            return
        order_detail = f"{menu_item} x {quantity}\n"
        self.order_details_text.insert(tk.END, order_detail)
    
    def display_order(self):
        # Clear existing orders in the display
        for item in self.order_table.get_children():
            self.order_table.delete(item)

        # Fetch and display orders
        for order in self.order_manager.get_orders():
            # Format order details for display
            order_details = ', '.join([f"{item.item_name} x {item.quantity}" for item in order.items])
            total_price = f"${order.calculate_total():.2f}"  # Calculate total price and format it as a string in dollars

            # Insert order into the table with the order's details and status
            self.order_table.insert('', 'end', values=(order.order_id, order.customer_name, order_details, order.status, total_price), tags=(order.status,))

            # Configure row colors based on the order status
            self.order_table.tag_configure('Preparing', foreground='orange')
            self.order_table.tag_configure('Delivered', foreground='green')

        # This ensures that the table is updated with the correct color coding
        self.order_table.update_idletasks()

        # Call this to ensure the changes take effect
        self.order_table.update()


   
    def add_order(self):
        order_id = self.order_id_entry.get()
        customer_name = self.customer_name_entry.get()
        # Retrieve order details from the text widget and format them as required
        order_details_raw = self.order_details_text.get("1.0", tk.END).strip()

        # Validate the input
        if not order_id or not customer_name or not order_details_raw:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Parse and format the raw order details
        try:
            items_data = []
            for line in order_details_raw.split('\n'):
                if line:
                    item_name, quantity = line.rsplit(' x ', 1)
                    price_per_item = self.menu_manager.get_price(item_name)
                    items_data.append({"item_name": item_name, "quantity": int(quantity), "price_per_item": price_per_item})

            order_details = json.dumps(items_data)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid order details format: {e}")
            return

        # Add the order
        try:
            self.order_manager.add_order(order_id, customer_name, order_details)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Refresh the order display
        self.display_order()

        # Optionally clear the input fields
        self.order_id_entry.delete(0, tk.END)
        self.customer_name_entry.delete(0, tk.END)
        self.order_details_text.delete("1.0", tk.END)

    def update_order(self):
        selected_item = self.order_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No order selected")
            return

        order_id = self.order_id_entry.get()
        new_customer_name = self.customer_name_entry.get()
        new_order_details_raw = self.order_details_text.get("1.0", tk.END).strip()

        # Parse and format the raw order details
        try:
            items_data = []
            for line in new_order_details_raw.split('\n'):
                if line:
                    item_name, quantity = line.rsplit(' x ', 1)
                    price_per_item = self.menu_manager.get_price(item_name)
                    items_data.append({"item_name": item_name, "quantity": int(quantity), "price_per_item": price_per_item})

            new_order_details = json.dumps(items_data)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid format for order details: {e}")
            return

        # Proceed with the update
        try:
            self.order_manager.update_order(order_id, new_customer_name, new_order_details)
            messagebox.showinfo("Success", "Order updated successfully")  # Success message
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.display_order()  # Corrected function call


    def delete_order(self):
        selected_item = self.order_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No order selected")
            return

        order_id = self.order_table.item(selected_item, 'values')[0]
        # Retrieve the order to check its status
        order = self.order_manager.get_order_by_id(order_id)
        if order.status == 'Delivered':
            messagebox.showerror("Error", "Delivered orders cannot be deleted.")
            return

        # If the order is not 'Delivered', proceed with deletion
        self.order_manager.delete_order(order_id)
        self.display_order()
        messagebox.showinfo("Success", f"Order {order_id} has been deleted.")

    def mark_as_delivered(self):
        selected_item = self.order_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No order selected")
            return

        order_id = self.order_table.item(selected_item, 'values')[0]
        self.order_manager.mark_order_as_delivered(order_id)  # This method will need to be implemented in the OrderManager class
        messagebox.showinfo("Success", f"Order {order_id} marked as Delivered")
        self.display_order()

    def print_receipt(self):
        selected_item = self.order_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No order selected for receipt")
            return

        # Retrieve the order ID from the selected row
        order_id = self.order_table.item(selected_item, 'values')[0]

        # Find the order from the order manager
        order = self.order_manager.get_order_by_id(order_id)
        if order is None:
            messagebox.showerror("Error", "Order not found")
            return

        # Generate receipt text
        receipt_text = f"Receipt for Order ID: {order_id}\nCustomer Name: {order.customer_name}\n\nOrder Details:\n"
        for item in order.items:
            receipt_text += f"{item.item_name} x {item.quantity} - ${item.price_per_item:.2f} each\n"
        receipt_text += f"\nTotal: ${order.calculate_total():.2f}"

        # Create a new Toplevel window to display the receipt
        receipt_window = tk.Toplevel(self.master)
        receipt_window.title(f"Receipt - Order {order_id}")
        receipt_window.geometry("400x300")

        # Add a Text widget to display the receipt
        receipt_display = tk.Text(receipt_window, height=15, width=50)
        receipt_display.pack(padx=10, pady=10)
        receipt_display.insert(tk.END, receipt_text)
        receipt_display.config(state='disabled')  # Make the text widget read-only



# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = OrderUI(root)
    root.mainloop()
