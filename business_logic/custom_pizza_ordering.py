import csv
import os
from typing import Dict, List

class CustomPizza:
    def __init__(self, base: str, sauce: str, toppings: List[str], size: str):
        self.base: str = base
        self.sauce: str = sauce
        self.toppings: List[str] = toppings
        self.size: str = size
        self.price: float = self.calculate_price()

    def calculate_price(self) -> float:
        base_price = 5.0  # Base price for a pizza
        topping_price = 0.5  # Price per topping

        # Price calculations can be more complex depending on the requirements
        price = base_price + topping_price * len(self.toppings)

        # Adjust price based on size
        size_multiplier = {'small': 1, 'medium': 1.5, 'large': 2}
        return price * size_multiplier.get(self.size, 1)

class CustomPizzaOrderManager:
    def __init__(self, data_file: str = 'custom_pizza_orders.csv'):
        self.data_file: str = data_file
        self.orders: List[CustomPizza] = []
        self.load_orders()

    def load_orders(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    base = row['base']
                    sauce = row['sauce']
                    toppings = row['toppings'].split(',')
                    size = row['size']
                    self.orders.append(CustomPizza(base, sauce, toppings, size))

    def save_orders(self) -> None:
        with open(self.data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['base', 'sauce', 'toppings', 'size', 'price'])
            writer.writeheader()
            for order in self.orders:
                writer.writerow({'base': order.base, 'sauce': order.sauce, 'toppings': ','.join(order.toppings), 'size': order.size, 'price': order.price})

    def add_order(self, base: str, sauce: str, toppings: List[str], size: str) -> None:
        new_order = CustomPizza(base, sauce, toppings, size)
        self.orders.append(new_order)
        self.save_orders()

    # Additional methods can be implemented as needed

# Example usage
if __name__ == "__main__":
    order_manager = CustomPizzaOrderManager()
    order_manager.add_order('Thin Crust', 'Tomato', ['Mozzarella', 'Basil'], 'large')
    for order in order_manager.orders:
        print(f"Order: Base - {order.base}, Sauce - {order.sauce}, Toppings - {', '.join(order.toppings)}, Size - {order.size}, Price - {order.price}")
