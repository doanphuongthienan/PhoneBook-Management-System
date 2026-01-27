from ui.console_utils import (
    print_header, print_subheader, pause, show_message, show_error, show_success,
    show_warning, display_contact, display_contacts_list, get_input, confirm, print_table
)
from services.auth_service import register, login, get_user_by_email, reset_password
from services.user_service import get_user_by_id, update_user_profile
from services.contact_service import (
    add_contact, view_contacts, get_contact_by_id, search_contacts, 
    sort_contacts, edit_contact, delete_contact, get_contacts_by_group
)
from services.group_service import (
    add_group, get_user_groups, get_group_by_name, delete_group, 
    add_contact_to_group, remove_contact_from_group, group_exists
)
from services.notification_service import (
    get_user_notifications, get_unread_notifications, mark_notification_as_read,
    mark_all_notifications_as_read, clear_user_notifications, check_birthdays
)
from services.import_export_service import (
    export_contacts, export_contacts_by_group, import_contacts, get_user_history, add_history_entry
)

# Global variable to track logged-in user
current_user = None


def main_menu():
    global current_user
    while True:
        print_header("Phone Book Management System")
        print("\n1. Login")
        print("2. Register")
        print("3. Forgot Password")
        print("4. Browse Contacts (as Guest)")
        print("0. Exit")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            login_menu()
        elif choice == "2":
            register_menu()
        elif choice == "3":
            forgot_password_menu()
        elif choice == "4":
            browse_contacts_guest()
        elif choice == "0":
            show_success("Thank you for using Phone Book Management System!")
            break
        else:
            show_error("Invalid choice")
            pause()


def register_menu():
    print_header("Register New Account")
    
    full_name = get_input("Full Name: ")
    email = get_input("Email: ", input_type="email")
    phone = get_input("Phone Number: ")
    password = get_input("Password (min 6 characters): ")
    confirm_password = get_input("Confirm Password: ")
    
    if password != confirm_password:
        show_error("Passwords do not match")
        pause()
        return
    
    success, msg = register(full_name, email, phone, password)
    if success:
        show_success(msg)
    else:
        show_error(msg)
    pause()


def login_menu():
    global current_user
    print_header("Login")
    
    email = get_input("Email: ", input_type="email")
    password = get_input("Password: ")
    
    success, user = login(email, password)
    if success:
        current_user = user
        show_success(f"Welcome back, {user.get('full_name')}!")
        check_birthdays(user.get('user_id'), user.get('email'))
        user_dashboard()
    else:
        show_error("Invalid email or password")
    pause()


def forgot_password_menu():
    print_header("Forgot Password")
    
    email = get_input("Enter your email: ", input_type="email")
    user = get_user_by_email(email)
    
    if not user:
        show_error("Email not found")
        pause()
        return
    
    show_message("Verification code sent to your email (demo mode)")
    new_password = get_input("Enter new password (min 6 characters): ")
    confirm_password = get_input("Confirm new password: ")
    
    if new_password != confirm_password:
        show_error("Passwords do not match")
        pause()
        return
    
    success, msg = reset_password(email, new_password)
    if success:
        show_success(msg)
    else:
        show_error(msg)
    pause()


def browse_contacts_guest():
    print_header("Browse Contacts (Guest Mode)")
    print("\nGuests can only search and view contacts.")
    print("Register or Login to add/edit/delete contacts.\n")
    
    while True:
        print("\n1. Search Contacts")
        print("2. View All Contacts")
        print("0. Back to Main Menu")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            keyword = get_input("Search keyword: ")
            print(f"\nSearching for: {keyword}")
            print("(Search available only to registered users)")
            show_message("Please register or login to search contacts")
        elif choice == "2":
            print_subheader("All Contacts Available in System")
            print("(View all available only to registered users)")
            show_message("Please register or login to view contacts")
        elif choice == "0":
            break
        else:
            show_error("Invalid choice")
        pause()


def user_dashboard():
    global current_user
    user_id = current_user.get('user_id')
    
    while True:
        print_header(f"Dashboard - {current_user.get('full_name')}")
        print("\n1. Manage Contacts")
        print("2. Manage Groups")
        print("3. Import/Export Contacts")
        print("4. View Notifications")
        print("5. Manage Profile")
        print("6. Logout")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            contact_menu(user_id)
        elif choice == "2":
            group_menu(user_id)
        elif choice == "3":
            import_export_menu(user_id)
        elif choice == "4":
            notification_menu(user_id)
        elif choice == "5":
            profile_menu(user_id)
        elif choice == "6":
            show_success("Logged out successfully")
            current_user = None
            pause()
            break
        else:
            show_error("Invalid choice")
            pause()


def contact_menu(user_id):
    while True:
        print_header("Contact Management")
        print("\n1. Add New Contact")
        print("2. View All Contacts")
        print("3. Search Contacts")
        print("4. View Contact Details")
        print("5. Edit Contact")
        print("6. Delete Contact")
        print("0. Back to Dashboard")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            add_contact_menu(user_id)
        elif choice == "2":
            view_all_contacts(user_id)
        elif choice == "3":
            search_contact_menu(user_id)
        elif choice == "4":
            view_contact_details(user_id)
        elif choice == "5":
            edit_contact_menu(user_id)
        elif choice == "6":
            delete_contact_menu(user_id)
        elif choice == "0":
            break
        else:
            show_error("Invalid choice")
            pause()


def add_contact_menu(user_id):
    print_header("Add New Contact")
    
    name = get_input("Contact Name: ")
    phone = get_input("Phone Number: ")
    email = get_input("Email: ", input_type="email")
    address = get_input("Address (optional): ", required=False)
    birthday = get_input("Birthday (YYYY-MM-DD, optional): ", required=False)
    notes = get_input("Notes (optional): ", required=False)
    
    contact = add_contact(name, phone, email, user_id, address, notes, birthday)
    
    show_success(f"Contact '{name}' added successfully!")
    
    # Ask about adding to groups
    if confirm("\nAdd contact to any groups? (y/n): "):
        groups = get_user_groups(user_id)
        if groups:
            print_subheader("Available Groups")
            for g in groups:
                print(f"- {g.get('name')}")
            
            while True:
                group_name = get_input("Enter group name (or 'done' to finish): ")
                if group_name.lower() == "done":
                    break
                
                success, msg = add_contact_to_group(contact.contact_id, group_name, user_id)
                if success:
                    show_success(msg)
                else:
                    show_error(msg)
    
    pause()


def view_all_contacts(user_id):
    print_header("All Contacts")
    
    contacts = view_contacts(user_id)
    
    if not contacts:
        show_message("No contacts found")
        pause()
        return
    
    # Show sort options
    print("\nSort by:")
    print("1. Name (A-Z)")
    print("2. Name (Z-A)")
    print("3. Created Date (Newest)")
    print("4. Created Date (Oldest)")
    
    choice = input("\nChoose sort option (1-4, or press Enter for default): ").strip()
    
    if choice == "1":
        contacts = sort_contacts(contacts, "name", ascending=True)
    elif choice == "2":
        contacts = sort_contacts(contacts, "name", ascending=False)
    elif choice == "3":
        contacts = sort_contacts(contacts, "created_at", ascending=False)
    elif choice == "4":
        contacts = sort_contacts(contacts, "created_at", ascending=True)
    
    display_contacts_list(contacts)
    pause()


def search_contact_menu(user_id):
    print_header("Search Contacts")
    
    print("\n1. Search by Name")
    print("2. Search by Phone")
    print("3. Search by Email")
    print("4. Search by Group")
    print("5. Search All Fields")
    
    choice = input("\nChoose search type: ").strip()
    
    search_type_map = {
        "1": "name",
        "2": "phone",
        "3": "email",
        "4": "group",
        "5": "all"
    }
    
    search_type = search_type_map.get(choice, "all")
    keyword = get_input("Enter search keyword: ")
    
    results = search_contacts(user_id, keyword, search_type)
    
    print_subheader(f"Search Results (found {len(results)} contacts)")
    display_contacts_list(results)
    pause()


def view_contact_details(user_id):
    print_header("View Contact Details")
    
    contacts = view_contacts(user_id)
    if not contacts:
        show_message("No contacts available")
        pause()
        return
    
    display_contacts_list(contacts, show_groups=False)
    
    contact_id = get_input("\nEnter Contact ID to view details: ", input_type="int")
    contact = get_contact_by_id(contact_id, user_id)
    
    if contact:
        display_contact(contact)
    else:
        show_error("Contact not found")
    
    pause()


def edit_contact_menu(user_id):
    print_header("Edit Contact")
    
    contacts = view_contacts(user_id)
    if not contacts:
        show_message("No contacts available")
        pause()
        return
    
    display_contacts_list(contacts, show_groups=False)
    
    contact_id = get_input("\nEnter Contact ID to edit: ", input_type="int")
    contact = get_contact_by_id(contact_id, user_id)
    
    if not contact:
        show_error("Contact not found")
        pause()
        return
    
    print_subheader("Edit Contact (Leave blank to keep current value)")
    
    name = get_input("Name: ", required=False) or contact.get("name")
    phone = get_input("Phone: ", required=False) or contact.get("phone")
    email = get_input("Email: ", required=False) or contact.get("email")
    address = get_input("Address: ", required=False) or contact.get("address")
    birthday = get_input("Birthday: ", required=False) or contact.get("birthday")
    notes = get_input("Notes: ", required=False) or contact.get("notes")
    
    success, msg = edit_contact(contact_id, user_id, name=name, phone=phone, email=email,
                               address=address, birthday=birthday, notes=notes)
    
    if success:
        show_success(msg)
    else:
        show_error(msg)
    pause()


def delete_contact_menu(user_id):
    print_header("Delete Contact")
    
    contacts = view_contacts(user_id)
    if not contacts:
        show_message("No contacts available")
        pause()
        return
    
    display_contacts_list(contacts, show_groups=False)
    
    contact_id = get_input("\nEnter Contact ID to delete: ", input_type="int")
    contact = get_contact_by_id(contact_id, user_id)
    
    if not contact:
        show_error("Contact not found")
        pause()
        return
    
    display_contact(contact)
    
    if confirm(f"\nAre you sure you want to delete '{contact.get('name')}'? (y/n): "):
        success, msg = delete_contact(contact_id, user_id)
        if success:
            show_success(msg)
        else:
            show_error(msg)
    
    pause()


def group_menu(user_id):
    while True:
        print_header("Group Management")
        
        groups = get_user_groups(user_id)
        print(f"\nYou have {len(groups)} group(s)")
        
        print("\n1. Create New Group")
        print("2. View Groups")
        print("3. Add Contact to Group")
        print("4. Remove Contact from Group")
        print("5. Delete Group")
        print("0. Back to Dashboard")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            create_group_menu(user_id)
        elif choice == "2":
            view_groups(user_id)
        elif choice == "3":
            add_to_group_menu(user_id)
        elif choice == "4":
            remove_from_group_menu(user_id)
        elif choice == "5":
            delete_group_menu(user_id)
        elif choice == "0":
            break
        else:
            show_error("Invalid choice")
            pause()


def create_group_menu(user_id):
    print_header("Create New Group")
    
    group_name = get_input("Group Name: ")
    
    if group_exists(group_name, user_id):
        show_error("Group already exists")
        pause()
        return
    
    group = add_group(group_name, user_id)
    show_success(f"Group '{group_name}' created successfully!")
    pause()


def view_groups(user_id):
    print_header("Your Groups")
    
    groups = get_user_groups(user_id)
    if not groups:
        show_message("No groups created yet")
        pause()
        return
    
    for g in groups:
        group_name = g.get('name')
        contacts = get_contacts_by_group(user_id, group_name)
        print(f"\n{g.get('group_id')}. {group_name} ({len(contacts)} contacts)")
    
    pause()


def add_to_group_menu(user_id):
    print_header("Add Contact to Group")
    
    groups = get_user_groups(user_id)
    if not groups:
        show_error("No groups available. Create a group first.")
        pause()
        return
    
    contacts = view_contacts(user_id)
    if not contacts:
        show_error("No contacts available")
        pause()
        return
    
    display_contacts_list(contacts)
    contact_id = get_input("\nEnter Contact ID: ", input_type="int")
    
    print_subheader("Available Groups")
    for g in groups:
        print(f"- {g.get('name')}")
    
    group_name = get_input("\nEnter Group Name: ")
    
    success, msg = add_contact_to_group(contact_id, group_name, user_id)
    if success:
        show_success(msg)
    else:
        show_error(msg)
    pause()


def remove_from_group_menu(user_id):
    print_header("Remove Contact from Group")
    
    groups = get_user_groups(user_id)
    if not groups:
        show_error("No groups available")
        pause()
        return
    
    print_subheader("Available Groups")
    for g in groups:
        print(f"- {g.get('name')}")
    
    group_name = get_input("\nEnter Group Name: ")
    
    contacts = get_contacts_by_group(user_id, group_name)
    if not contacts:
        show_error("No contacts in this group")
        pause()
        return
    
    display_contacts_list(contacts)
    contact_id = get_input("\nEnter Contact ID: ", input_type="int")
    
    from services.group_service import remove_contact_from_group
    success, msg = remove_contact_from_group(contact_id, group_name, user_id)
    if success:
        show_success(msg)
    else:
        show_error(msg)
    pause()


def delete_group_menu(user_id):
    print_header("Delete Group")
    
    groups = get_user_groups(user_id)
    if not groups:
        show_message("No groups available")
        pause()
        return
    
    print_subheader("Your Groups")
    for g in groups:
        print(f"- {g.get('name')}")
    
    group_name = get_input("\nEnter Group Name to delete: ")
    group = get_group_by_name(group_name, user_id)
    
    if not group:
        show_error("Group not found")
        pause()
        return
    
    if confirm(f"Are you sure you want to delete '{group_name}'? (y/n): "):
        success, msg = delete_group(group.get('group_id'), user_id)
        if success:
            show_success(msg)
        else:
            show_error(msg)
    
    pause()


def import_export_menu(user_id):
    while True:
        print_header("Import/Export Contacts")
        
        print("\n1. Export All Contacts")
        print("2. Export Contacts by Group")
        print("3. Import Contacts from File")
        print("4. View Import/Export History")
        print("0. Back to Dashboard")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            export_all_menu(user_id)
        elif choice == "2":
            export_by_group_menu(user_id)
        elif choice == "3":
            import_contacts_menu(user_id)
        elif choice == "4":
            view_history_menu(user_id)
        elif choice == "0":
            break
        else:
            show_error("Invalid choice")
            pause()


def export_all_menu(user_id):
    print_header("Export All Contacts")
    
    contacts = view_contacts(user_id)
    if not contacts:
        show_error("No contacts to export")
        pause()
        return
    
    filename = get_input("Enter filename (with .json extension): ")
    
    success, msg = export_contacts(contacts, filename)
    if success:
        show_success(msg)
        add_history_entry(user_id, "export", filename, len(contacts), "success")
    else:
        show_error(msg)
    pause()


def export_by_group_menu(user_id):
    print_header("Export Contacts by Group")
    
    groups = get_user_groups(user_id)
    if not groups:
        show_error("No groups available")
        pause()
        return
    
    print_subheader("Available Groups")
    for g in groups:
        print(f"- {g.get('name')}")
    
    group_name = get_input("\nEnter Group Name: ")
    filename = get_input("Enter filename (with .json extension): ")
    
    success, msg = export_contacts_by_group(user_id, group_name, filename)
    if success:
        show_success(msg)
        add_history_entry(user_id, "export", filename, 0, "success")
    else:
        show_error(msg)
    pause()


def import_contacts_menu(user_id):
    print_header("Import Contacts from File")
    
    filename = get_input("Enter filename to import: ")
    
    success, result = import_contacts(user_id, filename)
    if success:
        summary, details = result
        show_success(summary)
        
        if details.get("errors"):
            print_subheader("Import Errors")
            for error in details["errors"]:
                show_error(error)
        
        add_history_entry(user_id, "import", filename, details.get("success", 0), "success")
    else:
        show_error(result)
        add_history_entry(user_id, "import", filename, 0, "failed")
    pause()


def view_history_menu(user_id):
    print_header("Import/Export History")
    
    history = get_user_history(user_id)
    
    if not history:
        show_message("No import/export history")
        pause()
        return
    
    headers = ["Date", "Action", "File", "Count", "Status"]
    rows = []
    for h in history:
        timestamp = h.get("timestamp", "").split("T")[0]
        rows.append([
            timestamp,
            h.get("action", "").upper(),
            h.get("file_name", ""),
            h.get("count", ""),
            h.get("status", "").upper()
        ])
    
    print_table(headers, rows)
    pause()


def notification_menu(user_id):
    while True:
        print_header("Notifications")
        
        unread = get_unread_notifications(user_id)
        total = get_user_notifications(user_id)
        
        print(f"\nUnread: {len(unread)} | Total: {len(total)}")
        
        print("\n1. View All Notifications")
        print("2. View Unread Notifications")
        print("3. Mark All as Read")
        print("4. Clear All Notifications")
        print("0. Back to Dashboard")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            view_notifications(get_user_notifications(user_id))
        elif choice == "2":
            view_notifications(unread)
        elif choice == "3":
            mark_all_notifications_as_read(user_id)
            show_success("All notifications marked as read")
        elif choice == "4":
            if confirm("Clear all notifications? (y/n): "):
                clear_user_notifications(user_id)
                show_success("All notifications cleared")
        elif choice == "0":
            break
        else:
            show_error("Invalid choice")
        pause()


def view_notifications(notifications):
    print_header("Notifications")
    
    if not notifications:
        show_message("No notifications")
        return
    
    for n in notifications:
        status = "[UNREAD]" if not n.get("is_read") else "[READ]"
        print(f"\n{status} {n.get('notification_type', 'system').upper()}")
        print(f"Message: {n.get('message')}")
        print(f"Date: {n.get('created_at', '').split('T')[0]}")


def profile_menu(user_id):
    print_header("Manage Profile")
    
    user = get_user_by_id(user_id)
    if not user:
        show_error("User not found")
        pause()
        return
    
    print("\nCurrent Profile Information:")
    print(f"Full Name: {user.get('full_name')}")
    print(f"Email: {user.get('email')}")
    print(f"Phone: {user.get('phone')}")
    
    print("\n1. Update Full Name")
    print("2. Update Email")
    print("3. Update Phone")
    print("0. Back to Dashboard")
    
    choice = input("\nChoose an option: ").strip()
    
    if choice == "1":
        new_name = get_input("New Full Name: ")
        success, msg = update_user_profile(user_id, full_name=new_name)
        if success:
            show_success(msg)
            current_user['full_name'] = new_name
        else:
            show_error(msg)
    elif choice == "2":
        new_email = get_input("New Email: ", input_type="email")
        success, msg = update_user_profile(user_id, email=new_email)
        if success:
            show_success(msg)
            current_user['email'] = new_email
        else:
            show_error(msg)
    elif choice == "3":
        new_phone = get_input("New Phone: ")
        success, msg = update_user_profile(user_id, phone=new_phone)
        if success:
            show_success(msg)
            current_user['phone'] = new_phone
        else:
            show_error(msg)
    
    pause()

