import tkinter as tk
from ui.main_window import MainWindow

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Gautam's Pizza Store Application")
    # root.geometry("1000x800")  # You can adjust the size as needed

    # Initialize the main window class from ui/main_window.py
    app = MainWindow(root)

    # Start the Tkinter event loop
    root.mainloop()  # Call mainloop on the root object, not on app

if __name__ == "__main__":
    main()
