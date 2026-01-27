def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("Press Enter to continue...")


def print_header(title):
    clear_screen()
    print("=" * 60)
    print(title.center(60).upper())
    print("=" * 60)


def print_subheader(title):
    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)


def show_message(message, message_type="info"):
    """Display message with type indicator"""
    if message_type == "success":
        print(f"✓ {message}")
    elif message_type == "error":
        print(f"✗ {message}")
    elif message_type == "warning":
        print(f"! {message}")
    else:
        print(f"→ {message}")


def show_error(message):
    print(f"✗ ERROR: {message}")


def show_success(message):
    print(f"✓ SUCCESS: {message}")


def show_warning(message):
    print(f"! WARNING: {message}")


def print_table(headers, rows):
    """Print formatted table"""
    col_widths = [max(len(str(header)), max(len(str(row[i])) if i < len(row) else 0 for row in rows)) 
                  for i, header in enumerate(headers)]
    
    # Print header
    header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, col_widths))
    print(header_line)
    print("-" * len(header_line))
    
    # Print rows
    for row in rows:
        row_line = " | ".join(str(row[i] if i < len(row) else "").ljust(w) for i, w in enumerate(col_widths))
        print(row_line)


def get_input(prompt, input_type="string", required=True):
    """Get validated user input"""
    while True:
        try:
            value = input(prompt).strip()
            
            if required and not value:
                show_error("This field is required")
                continue
            
            if input_type == "int":
                return int(value)
            elif input_type == "float":
                return float(value)
            elif input_type == "email":
                import re
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(pattern, value):
                    return value
                show_error("Invalid email format")
                continue
            else:
                return value
        except ValueError:
            show_error(f"Invalid {input_type} format")


def confirm(prompt="Are you sure? (y/n): "):
    """Get yes/no confirmation"""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        show_error("Please enter 'y' or 'n'")


def display_contact(contact):
    """Display contact information in readable format"""
    print("\n" + "=" * 60)
    print(f"Name:    {contact.get('name', 'N/A')}")
    print(f"Phone:   {contact.get('phone', 'N/A')}")
    print(f"Email:   {contact.get('email', 'N/A')}")
    if contact.get('address'):
        print(f"Address: {contact.get('address')}")
    if contact.get('birthday'):
        print(f"Birthday: {contact.get('birthday')}")
    if contact.get('groups'):
        print(f"Groups:  {', '.join(contact.get('groups', []))}")
    if contact.get('notes'):
        print(f"Notes:   {contact.get('notes')}")
    print("=" * 60)


def display_contacts_list(contacts, show_groups=True):
    """Display list of contacts in table format"""
    if not contacts:
        show_message("No contacts found")
        return
    
    headers = ["ID", "Name", "Phone", "Email"]
    if show_groups:
        headers.append("Groups")
    
    rows = []
    for c in contacts:
        row = [
            c.get('contact_id'),
            c.get('name', 'N/A'),
            c.get('phone', 'N/A'),
            c.get('email', 'N/A')
        ]
        if show_groups:
            row.append(", ".join(c.get('groups', [])) or "-")
        rows.append(row)
    
    print_table(headers, rows)

