#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phone Book Management System
A comprehensive contact management system with user authentication,
contact organization, import/export functionality, and notifications.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.menu_handlers import main_menu
from ui.console_utils import print_header, show_success


def initialize_data_files():
    """Initialize JSON data files if they don't exist"""
    import json
    
    data_files = {
        "data/users.json": [],
        "data/contacts.json": [],
        "data/groups.json": [],
        "data/notifications.json": [],
        "data/import_export_history.json": []
    }
    
    for filepath, default_data in data_files.items():
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False)


def main():
    """Main entry point for the application"""
    try:
        # Initialize data files
        initialize_data_files()
        
        # Start the application
        main_menu()
    
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
