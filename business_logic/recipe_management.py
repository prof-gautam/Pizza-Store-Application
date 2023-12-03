import csv
import os
from typing import Dict, List, Tuple
from uuid import uuid4

class Recipe:
    def __init__(self, recipe_id: str, name: str, ingredients: Dict[str, str], category: str):
        self.recipe_id = recipe_id
        self.name = name
        self.ingredients = ingredients  # e.g., {'cheese': '100g', 'tomato': '50g'}
        self.category = category

class RecipeManager:
    def __init__(self, data_file: str = 'recipes.csv'):
        self.data_file = data_file
        self.recipes = {}
        self.load_recipes()

    def load_recipes(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    recipe_id = row['recipe_id']
                    name = row['name']
                    ingredients = eval(row['ingredients'])
                    category = row['category']
                    self.recipes[recipe_id] = Recipe(recipe_id, name, ingredients, category)

    def save_recipes(self) -> None:
        with open(self.data_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['recipe_id', 'name', 'ingredients', 'category']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for recipe in self.recipes.values():
                writer.writerow({'recipe_id': recipe.recipe_id, 'name': recipe.name, 'ingredients': str(recipe.ingredients), 'category': recipe.category})

    def add_recipe(self, name: str, ingredients: Dict[str, str], category: str) -> str:
        recipe_id = str(uuid4())
        self.recipes[recipe_id] = Recipe(recipe_id, name, ingredients, category)
        self.save_recipes()
        return recipe_id

    def edit_recipe(self, recipe_id: str, new_name: str = None, new_ingredients: Dict[str, str] = None, new_category: str = None) -> bool:
        if recipe_id in self.recipes:
            recipe = self.recipes[recipe_id]
            if new_name:
                recipe.name = new_name
            if new_ingredients:
                recipe.ingredients = new_ingredients
            if new_category:
                recipe.category = new_category
            self.save_recipes()
            return True
        return False

    def delete_recipe(self, recipe_id: str) -> bool:
        if recipe_id in self.recipes:
            del self.recipes[recipe_id]
            self.save_recipes()
            return True
        return False

    def find_recipe_by_id(self, recipe_id: str) -> Recipe:
        return self.recipes.get(recipe_id)

    def search_recipes(self, name: str = None, category: str = None) -> List[Recipe]:
        return [recipe for recipe in self.recipes.values() if (name is None or recipe.name == name) and (category is None or recipe.category == category)]

    # Additional methods can be implemented as needed

# Example usage
if __name__ == "__main__":
    manager = RecipeManager()
    recipe_id = manager.add_recipe('Margherita', {'cheese': '100g', 'tomato': '50g', 'basil': '5g'}, 'vegetarian')
    print(f"Added recipe ID: {recipe_id}")
    for recipe in manager.search_recipes(name='Margherita'):
        print(f"{recipe.name} ({recipe.recipe_id}): {recipe.ingredients}, Category: {recipe.category}")
