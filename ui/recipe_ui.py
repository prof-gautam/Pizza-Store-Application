import tkinter as tk
import json
from tkinter import ttk, messagebox
from business_logic import RecipeManager

class RecipeUI:
    def __init__(self, master):
        self.master = master
        self.recipe_manager = RecipeManager()
        self.setup_ui()

    def setup_ui(self):
        # Styling and layout configuration
        style = ttk.Style()
        style.configure('TButton', foreground='black', background='white')
        style.configure('Treeview', highlightthickness=0, bd=0, font=('Helvetica', 10))
        style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))

        # Labels and Entry fields for recipe details
        ttk.Label(self.master, text="Recipe Name:").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(self.master, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.master, text="Ingredients (JSON):").grid(row=1, column=0, padx=10, pady=10)
        self.ingredients_entry = ttk.Entry(self.master, width=30)
        self.ingredients_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.master, text="Category:").grid(row=2, column=0, padx=10, pady=10)
        self.category_entry = ttk.Entry(self.master, width=30)
        self.category_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons for adding, editing, and deleting recipes
        ttk.Button(self.master, text="Add Recipe", command=self.add_recipe).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.master, text="Edit Recipe", command=self.edit_recipe).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(self.master, text="Delete Recipe", command=self.delete_recipe).grid(row=3, column=2, padx=10, pady=10)
        

        # Treeview for displaying recipes
        self.recipe_table = ttk.Treeview(self.master, columns=("ID", "Name", "Ingredients", "Category"), show='headings')
        self.recipe_table.heading("ID", text="ID")
        self.recipe_table.heading("Name", text="Name")
        self.recipe_table.heading("Ingredients", text="Ingredients")
        self.recipe_table.heading("Category", text="Category")
        self.recipe_table.grid(row=4, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)
        self.recipe_table.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Configure grid layout
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        
        
        
        #search bar
        self.search_var = tk.StringVar()
        search_label = ttk.Label(self.master, text="Search Recipe:")
        search_label.grid(row=5, column=0, padx=10, pady=2, sticky='w')

        search_entry = ttk.Entry(self.master, textvariable=self.search_var)
        search_entry.grid(row=5, column=1, padx=10, pady=2, sticky='ew')

        search_button = ttk.Button(self.master, text="Search", command=self.search_recipes)
        search_button.grid(row=5, column=2, padx=10, pady=2)

        # Initial display of recipes
        self.display_recipes()

    def display_recipes(self):
        self.recipe_table.delete(*self.recipe_table.get_children())
        for recipe_id, recipe in self.recipe_manager.recipes.items():
            self.recipe_table.insert('', 'end', values=(recipe_id, recipe.name, json.dumps(recipe.ingredients), recipe.category))

    def on_tree_select(self, event):
        selection = self.recipe_table.focus()
        if selection:
            recipe = self.recipe_table.item(selection)['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, recipe[1])
            self.ingredients_entry.delete(0, tk.END)
            self.ingredients_entry.insert(0, recipe[2])
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, recipe[3])

    def add_recipe(self):
        name = self.name_entry.get()
        ingredients = self.ingredients_entry.get()
        category = self.category_entry.get()
        if not name or not ingredients or not category:
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            ingredients_dict = json.loads(ingredients)
            recipe_id = self.recipe_manager.add_recipe(name, ingredients_dict, category)
            messagebox.showinfo("Success", f"Recipe added with ID: {recipe_id}")
            self.display_recipes()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format for ingredients")

    def edit_recipe(self):
        selected = self.recipe_table.focus()
        if not selected:
            messagebox.showerror("Error", "No recipe selected")
            return
        recipe_id = self.recipe_table.item(selected)['values'][0]
        new_name = self.name_entry.get()
        new_ingredients = self.ingredients_entry.get()
        new_category = self.category_entry.get()
        try:
            new_ingredients_dict = json.loads(new_ingredients)
            self.recipe_manager.edit_recipe(recipe_id, new_name, new_ingredients_dict, new_category)
            messagebox.showinfo("Success", "Recipe updated")
            self.display_recipes()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format for ingredients")

    def delete_recipe(self):
        selected = self.recipe_table.focus()
        if not selected:
            messagebox.showerror("Error", "No recipe selected")
            return
        recipe_id = self.recipe_table.item(selected)['values'][0]
        confirm = messagebox.askyesno("Confirm", "Delete this recipe?")
        if confirm:
            self.recipe_manager.delete_recipe(recipe_id)
            messagebox.showinfo("Success", "Recipe deleted")
            self.display_recipes()
    def search_recipes(self):
            search_term = self.search_var.get().lower().strip()
            for child in self.recipe_table.get_children():
                self.recipe_table.delete(child)

            # Filter recipes based on the search term
            for recipe in self.recipe_manager.recipes:
                if search_term in recipe.name.lower():
                    self.recipe_table.insert('', 'end', values=(recipe.name, json.dumps(recipe.ingredients), recipe.category))

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Recipe Manager")
    root.geometry("800x600")
    app = RecipeUI(root)
    root.mainloop()
