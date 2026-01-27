"""
Phone Book Management System - Tkinter GUI Version
Main entry point for the GUI application
"""

import os
import json
from ui.tkinter_gui import PhoneBookApp


def initialize_data_files():
    """Initialize data files if they don't exist"""
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    files = {
        "users.json": [],
        "contacts.json": [],
        "groups.json": [],
        "notifications.json": [],
        "import_export_history.json": []
    }
    
    for filename, initial_data in files.items():
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump(initial_data, f, indent=4)


def main():
    """Start the Tkinter GUI application"""
    initialize_data_files()
    
    app = PhoneBookApp()
    app.mainloop()


if __name__ == "__main__":
    main()
