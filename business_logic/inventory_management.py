import csv
import os
from typing import Dict, List

class InventoryItem:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity

class InventoryManager:
    def __init__(self, data_file='inventory.csv'):
        self.data_file = data_file
        self.inventory = {}
        self.load_inventory()

    def load_inventory(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row['name']
                    quantity = int(row['quantity'])
                    self.inventory[name] = InventoryItem(name, quantity)

    def save_inventory(self):
        with open(self.data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'quantity'])
            writer.writeheader()
            for item in self.inventory.values():
                writer.writerow({'name': item.name, 'quantity': item.quantity})

    def add_item(self, name, quantity):
        self.inventory[name] = self.inventory.get(name, InventoryItem(name, 0))
        self.inventory[name].quantity += quantity
        self.save_inventory()

    def update_item(self, name, quantity):
        if name in self.inventory:
            self.inventory[name].quantity = quantity
            self.save_inventory()
            return True
        return False

    def deduct_stock(self, name, quantity):
        if name in self.inventory and self.inventory[name].quantity >= quantity:
            self.inventory[name].quantity -= quantity
            self.save_inventory()
            return True
        return False

    def delete_item(self, name):
        if name in self.inventory:
            del self.inventory[name]
            self.save_inventory()
            return True
        return False

    def get_low_stock_items(self, threshold=10):
        return [item for item in self.inventory.values() if item.quantity <= threshold]

    def check_and_alert_low_stock(self):
        low_stock_items = self.get_low_stock_items()
        for item in low_stock_items:
            print(f"Alert: {item.name} is low on stock ({item.quantity} remaining).")

# Example usage
if __name__ == "__main__":
    manager = InventoryManager()
    manager.add_item('Cheese', 50)
    manager.deduct_stock('Cheese', 10)  # Deducting stock as an example
    manager.check_and_alert_low_stock()  # Checking for low stock items
