import tkinter as tk
from tkinter import ttk

#imporing custom impotors
from ui.recipe_ui import RecipeUI
from ui.inventory_ui import InventoryUI
from ui.order_ui import OrderUI
from ui.menu_ui import MenuUI

#utils for program
from ui.utils import create_styled_button, show_error_message



class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Gautam's Pizza Store Application")
        self.master.geometry("800x600")  # Adjust the size as needed

        self.create_widgets()

    def create_widgets(self):
        # Create a tab control
        tab_control = ttk.Notebook(self.master)

        # Tabs for different functionalities
        recipe_tab = ttk.Frame(tab_control)
        inventory_tab = ttk.Frame(tab_control)
        order_tab = ttk.Frame(tab_control)
        menu_tab = ttk.Frame(tab_control)

        # Adding tabs to the notebook
        tab_control.add(recipe_tab, text='Recipes')
        tab_control.add(inventory_tab, text='Inventory')
        tab_control.add(order_tab, text='Orders')
        tab_control.add(menu_tab, text='Menu')

        # Pack the tab control
        tab_control.pack(expand=1, fill="both")

        # Call methods to populate each tab (placeholders for now)
        self.populate_recipe_tab(recipe_tab)
        self.populate_inventory_tab(inventory_tab)
        self.populate_order_tab(order_tab)
        self.populate_menu_tab(menu_tab)

        
    def populate_recipe_tab(self, tab):
        recipe_ui = RecipeUI(tab)

    def populate_inventory_tab(self, tab):
        inventory_ui = InventoryUI(tab)

    def populate_order_tab(self, tab):
        order_ui = OrderUI(tab)

    def populate_menu_tab(self, tab):
        menu_ui = MenuUI(tab)

# Test the window
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
