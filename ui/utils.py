import tkinter as tk
from tkinter import messagebox, ttk

# Common style settings
def create_styled_button(master, text, command, style='primary'):
    colors = {
        'primary': ('#0052cc', '#ffffff'),  # Blue background, white text
        'secondary': ('#e0e0e0', '#000000'),  # Grey background, black text
    }
    bg_color, fg_color = colors.get(style, colors['primary'])
    return tk.Button(master, text=text, command=command, bg=bg_color, fg=fg_color, padx=10, pady=5)

# Validation functions
def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_empty_field(field):
    return field.strip() == ''

# Data formatting
def format_currency(value):
    return f"${value:.2f}"

# Dialogs and popups
def show_error_message(message):
    messagebox.showerror("Error", message)

def confirm_action_dialog(message):
    return messagebox.askyesno("Confirm", message)

# Reusable custom widgets
class LabeledEntry(ttk.Frame):
    def __init__(self, master, label_text, **entry_kwargs):
        super().__init__(master)

        self.label = ttk.Label(self, text=label_text)
        self.label.pack(side=tk.LEFT, padx=(0, 10))

        self.entry = ttk.Entry(self, **entry_kwargs)
        self.entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    def get(self):
        return self.entry.get()

    def set(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

# Table for displaying lists of items
class SimpleTable(ttk.Frame):
    def __init__(self, master, columns, height=10):
        super().__init__(master)
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=height)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, stretch=tk.YES)
        self.tree.pack(side='top', fill='both', expand=True)

    def insert_row(self, row_data):
        self.tree.insert('', 'end', values=row_data)

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)



