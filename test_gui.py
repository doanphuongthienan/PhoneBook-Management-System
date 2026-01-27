"""
Test file for Tkinter GUI
Quick test to verify GUI is working correctly
"""

import os
import json
from ui.tkinter_gui import PhoneBookApp

def test_gui_imports():
    """Test that all GUI imports work"""
    try:
        from ui.tkinter_gui import (
            PhoneBookApp, LoginFrame, RegisterFrame, DashboardFrame,
            ContactManagementFrame, GroupManagementFrame, ImportExportFrame,
            NotificationFrame, ProfileFrame, COLORS
        )
        print("✓ All GUI imports successful")
        return True
    except Exception as e:
        print(f"✗ GUI import error: {e}")
        return False

def test_services_imports():
    """Test that all services are accessible"""
    try:
        from services.auth_service import register, login
        from services.contact_service import add_contact, view_contacts
        from services.group_service import add_group, get_user_groups
        from services.notification_service import get_user_notifications
        from services.import_export_service import export_contacts, import_contacts
        print("✓ All services imports successful")
        return True
    except Exception as e:
        print(f"✗ Services import error: {e}")
        return False

def test_data_files():
    """Test that data files exist and are valid"""
    data_files = [
        "data/users.json",
        "data/contacts.json",
        "data/groups.json",
        "data/notifications.json",
        "data/import_export_history.json"
    ]
    
    all_valid = True
    for filepath in data_files:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    json.load(f)
                print(f"✓ {filepath} is valid")
            except:
                print(f"✗ {filepath} is invalid JSON")
                all_valid = False
        else:
            print(f"✗ {filepath} not found")
            all_valid = False
    
    return all_valid

def test_colors():
    """Test color scheme"""
    from ui.tkinter_gui import COLORS
    
    required_colors = [
        'primary', 'secondary', 'accent', 'success', 'danger',
        'dark', 'light', 'text', 'bg', 'border'
    ]
    
    all_valid = True
    for color_name in required_colors:
        if color_name in COLORS:
            color_value = COLORS[color_name]
            if color_value.startswith('#') and len(color_value) == 7:
                print(f"✓ Color '{color_name}': {color_value}")
            else:
                print(f"✗ Invalid color value for '{color_name}': {color_value}")
                all_valid = False
        else:
            print(f"✗ Color '{color_name}' not found")
            all_valid = False
    
    return all_valid

def main():
    """Run all tests"""
    print("=" * 50)
    print("Tkinter GUI Test Suite")
    print("=" * 50)
    
    print("\n1. Testing GUI Imports...")
    print("-" * 50)
    test1 = test_gui_imports()
    
    print("\n2. Testing Services Imports...")
    print("-" * 50)
    test2 = test_services_imports()
    
    print("\n3. Testing Data Files...")
    print("-" * 50)
    test3 = test_data_files()
    
    print("\n4. Testing Color Scheme...")
    print("-" * 50)
    test4 = test_colors()
    
    print("\n" + "=" * 50)
    if all([test1, test2, test3, test4]):
        print("✓ All tests PASSED - GUI is ready to run!")
        print("\nTo start the GUI application, run:")
        print("  python main_gui.py")
    else:
        print("✗ Some tests FAILED - check errors above")
    print("=" * 50)

if __name__ == "__main__":
    main()
