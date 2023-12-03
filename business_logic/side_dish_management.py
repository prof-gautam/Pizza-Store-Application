import csv
import os
from typing import Dict, List

class SideDish:
    def __init__(self, name: str, description: str, price: float):
        self.name: str = name
        self.description: str = description
        self.price: float = price

class SideDishManager:
    def __init__(self, data_file: str = 'side_dishes.csv'):
        self.data_file: str = data_file
        self.side_dishes: Dict[str, SideDish] = {}
        self.load_side_dishes()

    def load_side_dishes(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name: str = row['name']
                    description: str = row['description']
                    price: float = float(row['price'])
                    self.side_dishes[name] = SideDish(name, description, price)

    def save_side_dishes(self) -> None:
        with open(self.data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'description', 'price'])
            writer.writeheader()
            for dish in self.side_dishes.values():
                writer.writerow({'name': dish.name, 'description': dish.description, 'price': dish.price})

    def add_side_dish(self, name: str, description: str, price: float) -> None:
        self.side_dishes[name] = SideDish(name, description, price)
        self.save_side_dishes()

    def update_side_dish(self, name: str, new_description: str = None, new_price: float = None) -> bool:
        if name in self.side_dishes:
            if new_description:
                self.side_dishes[name].description = new_description
            if new_price is not None:
                self.side_dishes[name].price = new_price
            self.save_side_dishes()
            return True
        return False

    def delete_side_dish(self, name: str) -> bool:
        if name in self.side_dishes:
            del self.side_dishes[name]
            self.save_side_dishes()
            return True
        return False

    def get_side_dishes(self) -> List[SideDish]:
        return list(self.side_dishes.values())

    # Additional methods can be implemented as needed

# Example usage
if __name__ == "__main__":
    side_dish_manager = SideDishManager()
    side_dish_manager.add_side_dish('Garlic Bread', 'Classic garlic bread', 3.99)
    for dish in side_dish_manager.get_side_dishes():
        print(f"{dish.name}: {dish.description}, Price: {dish.price}")
