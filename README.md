# Phone Book Management System

A comprehensive contact management system with user authentication, contact organization, import/export functionality, and notifications.

## Features

### 1. User Management
- **User Registration**: Register new accounts with email validation and password security
- **User Authentication**: Secure login with email and password
- **Password Reset**: Forgot password functionality with email verification
- **Profile Management**: Update personal information (name, email, phone)
- **User Account Security**: Passwords are hashed using SHA-256

### 2. Contact Management
- **Add Contacts**: Create new contacts with detailed information
  - Name, Phone, Email (required)
  - Address, Birthday, Notes (optional)
  - Assign to multiple groups
- **View Contacts**: Display all contacts in organized table format
- **Search Contacts**: Multiple search options
  - Search by name (partial keyword matching)
  - Search by phone number
  - Search by email address
  - Search by group name
  - Case-insensitive search
- **Sort Contacts**: Sort by name, creation date, or group
- **Edit Contacts**: Update existing contact information
- **Delete Contacts**: Remove contacts with confirmation
- **Detailed View**: View complete contact information including all fields

### 3. Contact Groups
- **Create Groups**: Organize contacts into custom groups (Family, Friends, Work, etc.)
- **Add to Groups**: Assign contacts to one or multiple groups
- **Remove from Groups**: Remove contacts from groups without deletion
- **Delete Groups**: Remove group categories
- **View by Group**: Display all contacts in a specific group

### 4. Import and Export
- **Export Contacts**: Save all contacts to JSON file for backup
- **Export by Group**: Export specific group's contacts
- **Import Contacts**: Import contacts from JSON files
  - Validates contact data
  - Checks for duplicate entries
  - Detailed import report with error tracking
- **Import History**: Track all import/export operations with timestamps

### 5. Notifications and Reminders
- **Contact Creation Notifications**: Automatic notification when contact is created
- **Birthday Reminders**: System checks and notifies on contact birthdays
- **Email Notifications**: Send notifications via email (demo mode)
- **In-System Notifications**: Store notifications in the system
- **Notification Management**: View, read, and clear notifications

### 6. Guest Access
- Browse and search contacts without creating an account
- Limited functionality - registration required to add/edit/delete

## Technical Stack

- **Language**: Python 3.12+
- **Database**: JSON files (local storage)
- **Security**: SHA-256 password hashing
- **Architecture**: Service-oriented architecture with clear separation of concerns

## Project Structure

```
PhoneBook-Management-System/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── models/                          # Data models
│   ├── __init__.py
│   ├── user_model.py               # User model
│   ├── contact_model.py            # Contact model
│   ├── group_model.py              # Group model
│   ├── notification_model.py       # Notification model
│   └── contact_group_model.py      # Contact-Group relationship
│
├── services/                        # Business logic services
│   ├── __init__.py
│   ├── auth_service.py             # Authentication & authorization
│   ├── user_service.py             # User profile management
│   ├── contact_service.py          # Contact operations
│   ├── group_service.py            # Group operations
│   ├── notification_service.py     # Notification management
│   └── import_export_service.py    # Import/export operations
│
├── ui/                             # User interface
│   ├── __init__.py
│   ├── console_utils.py            # Console utilities (display, input)
│   └── menu_handlers.py            # Menu navigation and handlers
│
└── data/                           # Data storage (JSON files)
    ├── users.json                  # User accounts
    ├── contacts.json               # Contact information
    ├── groups.json                 # Contact groups
    ├── notifications.json          # User notifications
    └── import_export_history.json  # Import/export records
```

## Installation and Setup

### Prerequisites
- Python 3.12 or higher
- Command line/Terminal access

### Step 1: Clone or Download the Project
```bash
cd PhoneBook-Management-System
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

The system uses only Python standard library by default. Optional dependencies can be uncommented in `requirements.txt` for enhanced security.

## Running the Application

### Start the Application
```bash
python main.py
```

### Initial Setup
On first run, the system will automatically create the data directory and initialize JSON files.

## Usage Guide

### Main Menu
1. **Login** - Sign in with existing account
2. **Register** - Create a new account
3. **Forgot Password** - Reset password
4. **Browse Contacts** - View contacts as guest
5. **Exit** - Close application

### After Login - Dashboard
1. **Manage Contacts**
   - Add new contacts
   - View all contacts
   - Search contacts
   - View contact details
   - Edit contact information
   - Delete contacts

2. **Manage Groups**
   - Create new groups
   - View groups
   - Add contacts to groups
   - Remove contacts from groups
   - Delete groups

3. **Import/Export**
   - Export all contacts
   - Export contacts by group
   - Import contacts from file
   - View import/export history

4. **View Notifications**
   - See all notifications
   - View unread notifications
   - Mark as read
   - Clear notifications

5. **Manage Profile**
   - Update full name
   - Update email
   - Update phone number

## Default Test Accounts

You can create your own account, or use the system with guest mode for browsing.

## Data Validation

### Email Validation
- Checks for valid email format (user@domain.com)
- Prevents duplicate email registration

### Password Validation
- Minimum 6 characters required
- Stored as SHA-256 hash for security

### Contact Data
- Name, Phone, Email are required fields
- Email format is validated
- Duplicate phone/email checking during import

## Sample Data Import Format

Import contacts using JSON format:
```json
[
  {
    "name": "John Doe",
    "phone": "555-1234",
    "email": "john@example.com",
    "address": "123 Main St",
    "birthday": "1990-05-15",
    "notes": "Best friend",
    "groups": ["Friends", "Work"]
  }
]
```

## Features Implemented

### Requirement 1: Search and View Contact Information ✓
- Multiple search criteria (name, phone, email, group)
- Partial keyword matching with case-insensitive search
- Sort by name (A-Z, Z-A), creation date, or group
- Detailed view of contact information
- Guest browsing capability

### Requirement 2: Register and Manage User Accounts ✓
- User registration with validation
- Duplicate email prevention
- Password security requirements
- User authentication (login/logout)
- Profile management with update capabilities
- Password reset with email verification (demo mode)
- Secure password storage with hashing

### Requirement 3: Add, Edit, and Delete Contacts ✓
- Add contacts with all required and optional fields
- Edit existing contact information
- Delete with confirmation to prevent accidental deletion
- Authenticated users only

### Requirement 4: Manage Contact Groups ✓
- Create custom contact groups
- Assign contacts to multiple groups
- Remove contacts from groups without deletion
- Group information storage and management

### Requirement 5: Import and Export Contacts ✓
- Import from JSON files
- Export to JSON files (all or by group)
- Data validation during import
- Duplicate checking
- Import/export history tracking
- Detailed error reporting

### Requirement 6: Notifications and Reminders ✓
- Birthday reminders (automatic checking)
- Contact creation notifications
- Email notification simulation
- In-system notifications
- Notification management (view, read, clear)

## Security Features

1. **Password Hashing**: SHA-256 encryption for passwords
2. **Email Validation**: Prevents invalid email addresses
3. **Duplicate Prevention**: Checks for existing emails and phone numbers
4. **Input Validation**: All user inputs are validated
5. **User Confirmation**: Deletion requires confirmation

## Limitations and Future Enhancements

Current Limitations:
- Local JSON-based storage (not scalable for enterprise use)
- Email notifications are in demo mode (console output)
- Single-user demonstration mode

Future Enhancements:
- Database integration (PostgreSQL, MongoDB)
- Real email sending capabilities
- Multi-user support with proper access control
- Contact photo storage
- Advanced analytics and reporting
- REST API for third-party integration
- Mobile application
- Dark theme support
- Contact synchronization

## Troubleshooting

### Issue: Data files are empty
**Solution**: Run `main.py` which will initialize data files automatically.

### Issue: Import fails with validation errors
**Solution**: Check JSON file format matches the required structure. Review error messages for specific field issues.

### Issue: Cannot login
**Solution**: 
- Verify email address is correct
- Check password is correct
- Ensure account is registered (use Register option)

## File Format Details

### User Storage (users.json)
```json
{
  "user_id": 1,
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234",
  "password": "hashed_password_here",
  "created_at": "2026-01-27T10:00:00"
}
```

### Contact Storage (contacts.json)
```json
{
  "contact_id": 1,
  "name": "Jane Smith",
  "phone": "555-5678",
  "email": "jane@example.com",
  "owner_id": 1,
  "address": "456 Oak Ave",
  "notes": "Best friend",
  "birthday": "1992-03-20",
  "groups": ["Friends", "Work"],
  "created_at": "2026-01-27T10:00:00",
  "updated_at": "2026-01-27T10:00:00"
}
```

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please review the requirements and documentation above. The system implements all specified functional requirements.

---

**Version**: 1.0  
**Last Updated**: January 27, 2026  
**Status**: Complete and Functional
