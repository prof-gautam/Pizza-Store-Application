import csv
import os
from typing import Dict, List

class MenuItem:
    def __init__(self, name: str, description: str, price: float):
        self.name: str = name
        self.description: str = description
        self.price: float = price

class MenuManager:
    def __init__(self, data_file: str = 'menu.csv'):
        self.data_file: str = data_file
        self.menu_items: Dict[str, MenuItem] = {}
        self.load_menu()

    def load_menu(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name: str = row['name']
                    description: str = row['description']
                    price: float = float(row['price'])
                    self.menu_items[name] = MenuItem(name, description, price)

    def save_menu(self) -> None:
        with open(self.data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'description', 'price'])
            writer.writeheader()
            for item in self.menu_items.values():
                writer.writerow({'name': item.name, 'description': item.description, 'price': item.price})

    def add_menu_item(self, name: str, description: str, price: float) -> None:
        self.menu_items[name] = MenuItem(name, description, price)
        self.save_menu()

    def update_menu_item(self, name: str, new_description: str = None, new_price: float = None) -> bool:
        if name in self.menu_items:
            if new_description:
                self.menu_items[name].description = new_description
            if new_price is not None:
                self.menu_items[name].price = new_price
            self.save_menu()
            return True
        return False

    def delete_menu_item(self, name: str) -> bool:
        if name in self.menu_items:
            del self.menu_items[name]
            self.save_menu()
            return True
        return False

    def get_menu_items(self) -> List[MenuItem]:
        return list(self.menu_items.values())

    # Additional methods can be implemented as needed
    
    def get_price(self, item_name):
        # Check if the item exists in the menu_items dictionary
        if item_name in self.menu_items:
            return self.menu_items[item_name].price
        else:
            # If the item is not found, you can choose to return None or raise an exception
            raise ValueError(f"Price not found for item '{item_name}'")


# Example usage
if __name__ == "__main__":
    menu_manager = MenuManager()
    menu_manager.add_menu_item('Margherita', 'Classic Margherita pizza with fresh basil', 12.99)
    for item in menu_manager.get_menu_items():
        print(f"{item.name}: {item.description}, Price: {item.price}")
