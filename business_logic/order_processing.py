import csv
import os
import json
from typing import Dict, List, Optional

class OrderItem:
    def __init__(self, item_name: str, quantity: int, price_per_item: float):
        self.item_name = item_name
        self.quantity = quantity
        self.price_per_item = price_per_item

    def total_price(self) -> float:
        return self.quantity * self.price_per_item

class Order:
    def __init__(self, order_id: str, customer_name: str, items: List[OrderItem], status: str = "Preparing"):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items
        self.status = status

    def calculate_total(self) -> float:
        return sum(item.total_price() for item in self.items)

class OrderManager:
    def __init__(self, data_file: str = 'orders.csv'):
        self.data_file = data_file
        self.orders: Dict[str, Order] = {}
        self.load_orders()

    def load_orders(self):
        if not os.path.exists(self.data_file):
            return

        with open(self.data_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                order_id = row['order_id']
                customer_name = row.get('customer_name', 'Unknown Customer')
                status = row.get('status', 'Preparing')
                items = self._parse_items(row['items'])
                self.orders[order_id] = Order(order_id, customer_name, items, status)

    def _parse_items(self, items_str: str) -> List[OrderItem]:
        items_data = json.loads(items_str)
        return [OrderItem(item['item_name'], item['quantity'], item['price_per_item']) for item in items_data]

    def save_orders(self):
        try:
            with open(self.data_file, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['order_id', 'customer_name', 'items', 'status']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for order in self.orders.values():
                    # Serialize the items list to a JSON string
                    items_data = json.dumps([{"item_name": item.item_name, 
                                            "quantity": item.quantity, 
                                            "price_per_item": item.price_per_item} 
                                            for item in order.items])
                    # Write the order data to the CSV file
                    writer.writerow({
                        'order_id': order.order_id, 
                        'customer_name': order.customer_name, 
                        'items': items_data, 
                        'status': order.status
                    })
        except IOError as e:
            # Handle the error (e.g., log it, notify the user, etc.)
            print(f"An error occurred while saving orders: {e}")


    def add_order(self, order_id: str, customer_name: str, order_details: str):
        if order_id in self.orders:
            raise ValueError("Order ID already exists.")

        items = self._parse_items(order_details)
        self.orders[order_id] = Order(order_id, customer_name, items)
        self.save_orders()

    def update_order(self, order_id: str, customer_name: str, order_details: str, status: Optional[str] = None):
        if order_id not in self.orders:
            raise ValueError("Order ID does not exist.")

        items = self._parse_items(order_details)
        order = self.orders[order_id]
        order.customer_name = customer_name
        order.items = items
        if status:
            order.status = status
        self.save_orders()

    def delete_order(self, order_id: str):
        if order_id not in self.orders:
            raise ValueError("Order ID does not exist.")

        del self.orders[order_id]
        self.save_orders()

    def get_orders(self) -> List[Order]:
        return list(self.orders.values())
    
    def get_order_by_id(self, order_id):
        return self.orders.get(order_id)

    
    def mark_order_as_delivered(self, order_id):
        if order_id not in self.orders:
            raise ValueError("Order ID does not exist.")
        self.orders[order_id].status = 'Delivered'
        self.save_orders()

# Example usage
if __name__ == "__main__":
    order_manager = OrderManager()
    order_details = json.dumps([{"item_name": "Margherita Pizza", "quantity": 2, "price_per_item": 12.99}, {"item_name": "Garlic Bread", "quantity": 1, "price_per_item": 3.99}])
    order_manager.add_order('order_001', 'Customer1', order_details)
    for order in order_manager.get_orders():
        print(f"Order ID: {order.order_id}, Customer: {order.customer_name}, Total Price: {order.calculate_total()}")
