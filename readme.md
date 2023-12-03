pizza_store_app/
│
├── main.py                   # Main application file
│
├── ui/
│   ├── __init__.py           # Makes UI a Python package
│   ├── main_window.py        # Code for the main window
│   ├── recipe_ui.py          # UI for recipe management
│   ├── inventory_ui.py       # UI for inventory management
│   ├── menu_ui.py            # UI for menu management
│   ├── order_ui.py           # UI for order processing
│   └── utils.py              # Common UI utilities and components
│
├── business_logic/
│   ├── __init__.py           # Makes business_logic a Python package
│   ├── recipe_logic.py       # Business logic for recipes
│   ├── inventory_logic.py    # Business logic for inventory
│   ├── menu_logic.py         # Business logic for menu
│   └── order_logic.py        # Business logic for orders
│
├── data/
│   ├── __init__.py           # Makes data a Python package
│   ├── data_manager.py       # Manages data storage and retrieval
│   └── sample_data/          # Folder for CSV data files
│       ├── recipes.csv       # CSV file for recipes
│       ├── inventory.csv     # CSV file for inventory
│       └── orders.csv        # CSV file for orders
│
└── tests/
    ├── __init__.py           # Makes tests a Python package
    └── test_cases.py         # Test cases for the application
