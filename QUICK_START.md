# Quick Start Guide - Phone Book Management System

## Getting Started in 5 Minutes

### 1. Start the Application
```bash
python main.py
```

### 2. Main Menu Options

#### Option A: Register New Account
```
Choose: 2
- Full Name: Your Name
- Email: your.email@example.com
- Phone: 555-1234
- Password: SecurePassword123
```

#### Option B: Login (if already registered)
```
Choose: 1
- Email: your.email@example.com
- Password: YourPassword
```

#### Option C: Browse as Guest
```
Choose: 4
- Limited search and view capabilities
```

### 3. Once Logged In - Dashboard Features

#### Add Your First Contact
```
1 -> 1 (Manage Contacts -> Add New Contact)
- Contact Name: Jane Doe
- Phone Number: 555-0123
- Email: jane@example.com
- Address: 123 Main St (optional)
- Birthday: 1990-05-15 (optional, YYYY-MM-DD format)
- Notes: My friend (optional)
- Add to groups? (y/n)
```

#### Search Contacts
```
1 -> 3 (Manage Contacts -> Search Contacts)
- Choose search type (by name, phone, email, group, or all)
- Enter keyword: "Jane"
```

#### Create a Group
```
2 -> 1 (Manage Groups -> Create New Group)
- Group Name: Friends
```

#### Add Contact to Group
```
2 -> 3 (Manage Groups -> Add Contact to Group)
- Select contact and group
```

#### Export Contacts
```
3 -> 1 (Import/Export -> Export All Contacts)
- Enter filename: my_contacts.json
```

#### Import Contacts
```
3 -> 3 (Import/Export -> Import from File)
- Enter filename: my_contacts.json
```

#### View Notifications
```
4 (View Notifications)
- See birthday reminders and contact creation confirmations
```

### 4. Common Tasks

**Search for a Contact**
- Dashboard → Manage Contacts → Search Contacts → Choose search type → Enter keyword

**Edit Contact Information**
- Dashboard → Manage Contacts → Edit Contact → Select contact ID → Update fields

**Delete a Contact**
- Dashboard → Manage Contacts → Delete Contact → Select contact → Confirm deletion

**Update Your Profile**
- Dashboard → Manage Profile → Choose field to update

**Change Password**
- Main Menu → Forgot Password → Enter email → Enter new password

## Menu Structure

```
MAIN MENU
├── 1. Login
├── 2. Register
├── 3. Forgot Password
├── 4. Browse Contacts (Guest)
└── 0. Exit

DASHBOARD (After Login)
├── 1. Manage Contacts
│   ├── 1. Add New Contact
│   ├── 2. View All Contacts
│   ├── 3. Search Contacts
│   ├── 4. View Contact Details
│   ├── 5. Edit Contact
│   ├── 6. Delete Contact
│   └── 0. Back
├── 2. Manage Groups
│   ├── 1. Create New Group
│   ├── 2. View Groups
│   ├── 3. Add Contact to Group
│   ├── 4. Remove Contact from Group
│   ├── 5. Delete Group
│   └── 0. Back
├── 3. Import/Export
│   ├── 1. Export All Contacts
│   ├── 2. Export by Group
│   ├── 3. Import from File
│   ├── 4. View History
│   └── 0. Back
├── 4. View Notifications
├── 5. Manage Profile
├── 6. Logout
└── 0. Exit
```

## Keyboard Input Guide

| Key | Action |
|-----|--------|
| Enter | Confirm input, continue |
| y/n | Yes/No answers |
| 0 | Go back to previous menu |
| q | Quit application (from main menu) |

## Sample Workflow

### Complete Registration and Add First Contact

1. Start app: `python main.py`
2. Choose: `2` (Register)
3. Fill in details:
   - Full Name: `John Smith`
   - Email: `john.smith@example.com`
   - Phone: `555-9876`
   - Password: `Password123`
4. Choose: `1` (Manage Contacts)
5. Choose: `1` (Add New Contact)
6. Enter contact info:
   - Name: `Alice Johnson`
   - Phone: `555-1111`
   - Email: `alice@example.com`
   - Address: `789 Elm St`
   - Birthday: `1995-07-20`
   - Notes: `Work colleague`
7. Add to group? `y`
8. Create group: `Work`
9. View your contacts: Back to Dashboard → Manage Contacts → View All Contacts

## Keyboard Shortcuts (in applicable menus)

- **Press 0** anytime to go back
- **Press 6** in dashboard to logout
- **Press 0** in main menu to exit

## Data Format for Import

Create a JSON file (e.g., `contacts.json`) with this format:

```json
[
  {
    "name": "Contact Name",
    "phone": "555-1234",
    "email": "contact@example.com",
    "address": "123 Main Street",
    "birthday": "1990-05-15",
    "notes": "Some notes",
    "groups": ["Friends", "Work"]
  },
  {
    "name": "Another Contact",
    "phone": "555-5678",
    "email": "another@example.com",
    "address": "456 Oak Avenue",
    "birthday": "1992-08-20",
    "notes": "Family member",
    "groups": ["Family"]
  }
]
```

## Tips & Tricks

1. **Search is case-insensitive**: Search for "john" or "JOHN" - both work
2. **Partial matching**: Search "john" finds "John Smith", "Johnson", etc.
3. **Multiple groups**: A contact can belong to several groups
4. **Birthday format**: Use YYYY-MM-DD (e.g., 1990-05-15)
5. **Phone format**: Any format works (555-1234, +1-555-1234, etc.)

## Common Error Messages & Solutions

| Error | Solution |
|-------|----------|
| Invalid email format | Use format: user@domain.com |
| Email already registered | Use different email or login |
| Password too short | Password must be at least 6 characters |
| Contact not found | Check contact ID and try again |
| Group already exists | Use different group name |
| No contacts available | Add contacts first |

## Features Checklist

- [x] User Registration with email validation
- [x] User Login/Logout
- [x] Password reset (forgot password)
- [x] Add/Edit/Delete Contacts
- [x] Search contacts (multiple criteria)
- [x] Sort contacts (name, date, group)
- [x] Create and manage groups
- [x] Import/Export contacts
- [x] Notifications system
- [x] Profile management

## Support

If you encounter any issues:

1. Check that data files exist in `/data` folder
2. Verify Python version is 3.12 or higher
3. Review README.md for detailed feature documentation
4. Check input formats for dates and emails

---

**Ready to use!** Start with `python main.py` and explore all features.
