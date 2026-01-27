# API Reference - Phone Book Management System

## Overview
This document provides detailed API reference for the Phone Book Management System services.

## Authentication Service (`services/auth_service.py`)

### Functions

#### `validate_email(email: str) -> bool`
Validates email format using regex pattern.
- **Parameters**: email (string)
- **Returns**: True if valid, False otherwise
- **Example**: `validate_email("user@example.com")` → True

#### `validate_password(password: str) -> tuple(bool, str)`
Validates password meets security requirements (minimum 6 characters).
- **Parameters**: password (string)
- **Returns**: (is_valid: bool, message: str)
- **Example**: `validate_password("short")` → (False, "Password must be at least 6 characters...")

#### `hash_password(password: str) -> str`
Hashes password using SHA-256 encryption.
- **Parameters**: password (string)
- **Returns**: hashed password (hex string)

#### `verify_password(password: str, hashed_password: str) -> bool`
Verifies plain password against stored hash.
- **Parameters**: password, hashed_password (strings)
- **Returns**: True if match, False otherwise

#### `email_exists(email: str) -> bool`
Checks if email is already registered.
- **Parameters**: email (string)
- **Returns**: True if exists, False otherwise

#### `register(full_name: str, email: str, phone: str, password: str) -> tuple(bool, str)`
Registers new user account with validation.
- **Parameters**: full_name, email, phone, password (strings)
- **Returns**: (success: bool, message: str)
- **Raises**: None (returns error in tuple)

#### `login(email: str, password: str) -> tuple(bool, dict | None)`
Authenticates user login.
- **Parameters**: email, password (strings)
- **Returns**: (success: bool, user_dict or None)
- **Returns user dict**: {user_id, full_name, email, phone, password, created_at}

#### `get_user_by_email(email: str) -> dict | None`
Retrieves user record by email.
- **Parameters**: email (string)
- **Returns**: user dict or None if not found

#### `reset_password(email: str, new_password: str) -> tuple(bool, str)`
Resets user password.
- **Parameters**: email, new_password (strings)
- **Returns**: (success: bool, message: str)

---

## Contact Service (`services/contact_service.py`)

### Functions

#### `add_contact(name, phone, email, owner_id, address="", notes="", birthday=None, groups=None) -> Contact`
Creates new contact.
- **Parameters**: 
  - name, phone, email, owner_id (required)
  - address, notes, birthday, groups (optional)
- **Returns**: Contact object
- **Example**: `add_contact("John", "555-1234", "john@ex.com", user_id)`

#### `view_contacts(owner_id: int) -> list`
Retrieves all contacts for a user.
- **Parameters**: owner_id (integer)
- **Returns**: List of contact dictionaries

#### `get_contact_by_id(contact_id: int, owner_id: int) -> dict | None`
Gets specific contact by ID.
- **Parameters**: contact_id, owner_id (integers)
- **Returns**: Contact dict or None

#### `search_contacts(owner_id: int, keyword: str, search_type="all") -> list`
Searches contacts with multiple criteria.
- **Parameters**: 
  - owner_id (integer)
  - keyword (string)
  - search_type: "all", "name", "phone", "email", "group" (string, default="all")
- **Returns**: List of matching contacts
- **Features**: Case-insensitive, partial keyword matching

#### `sort_contacts(contacts: list, sort_by="name", ascending=True) -> list`
Sorts contacts by specified field.
- **Parameters**:
  - contacts (list)
  - sort_by: "name", "created_at", "group" (string, default="name")
  - ascending (boolean, default=True)
- **Returns**: Sorted list of contacts

#### `edit_contact(contact_id: int, owner_id: int, **kwargs) -> tuple(bool, str)`
Updates contact information.
- **Parameters**: contact_id, owner_id, and any fields to update (name, phone, email, address, notes, birthday, groups)
- **Returns**: (success: bool, message: str)
- **Example**: `edit_contact(1, user_id, name="New Name", phone="555-9999")`

#### `delete_contact(contact_id: int, owner_id: int) -> tuple(bool, str)`
Deletes contact permanently.
- **Parameters**: contact_id, owner_id (integers)
- **Returns**: (success: bool, message: str)

#### `get_contacts_by_group(owner_id: int, group_name: str) -> list`
Gets all contacts in a specific group.
- **Parameters**: owner_id, group_name (integer, string)
- **Returns**: List of contacts in group

#### `check_duplicate(owner_id: int, phone: str, email: str) -> bool`
Checks if contact with same phone or email exists.
- **Parameters**: owner_id, phone, email (integer, strings)
- **Returns**: True if duplicate found, False otherwise

---

## Group Service (`services/group_service.py`)

### Functions

#### `add_group(name: str, owner_id: int) -> Group`
Creates new contact group.
- **Parameters**: name (string), owner_id (integer)
- **Returns**: Group object

#### `get_user_groups(owner_id: int) -> list`
Retrieves all groups for user.
- **Parameters**: owner_id (integer)
- **Returns**: List of group dictionaries

#### `get_group_by_id(group_id: int, owner_id: int) -> dict | None`
Gets specific group by ID.
- **Parameters**: group_id, owner_id (integers)
- **Returns**: Group dict or None

#### `get_group_by_name(name: str, owner_id: int) -> dict | None`
Gets group by name.
- **Parameters**: name (string), owner_id (integer)
- **Returns**: Group dict or None

#### `group_exists(name: str, owner_id: int) -> bool`
Checks if group name exists.
- **Parameters**: name (string), owner_id (integer)
- **Returns**: True if exists, False otherwise

#### `delete_group(group_id: int, owner_id: int) -> tuple(bool, str)`
Deletes group.
- **Parameters**: group_id, owner_id (integers)
- **Returns**: (success: bool, message: str)

#### `rename_group(group_id: int, owner_id: int, new_name: str) -> tuple(bool, str)`
Renames group.
- **Parameters**: group_id, owner_id (integers), new_name (string)
- **Returns**: (success: bool, message: str)

#### `add_contact_to_group(contact_id: int, group_name: str, owner_id: int) -> tuple(bool, str)`
Adds contact to group.
- **Parameters**: contact_id, owner_id (integers), group_name (string)
- **Returns**: (success: bool, message: str)

#### `remove_contact_from_group(contact_id: int, group_name: str, owner_id: int) -> tuple(bool, str)`
Removes contact from group.
- **Parameters**: contact_id, owner_id (integers), group_name (string)
- **Returns**: (success: bool, message: str)

---

## Import/Export Service (`services/import_export_service.py`)

### Functions

#### `export_contacts(contacts: list, filename: str) -> tuple(bool, str)`
Exports contacts to JSON file.
- **Parameters**: contacts (list), filename (string)
- **Returns**: (success: bool, message: str)
- **Example**: `export_contacts(contacts, "my_contacts.json")`

#### `export_contacts_by_group(user_id: int, group_name: str, filename: str) -> tuple(bool, str)`
Exports specific group's contacts.
- **Parameters**: user_id (integer), group_name (string), filename (string)
- **Returns**: (success: bool, message: str)

#### `import_contacts(user_id: int, filename: str) -> tuple(bool, tuple | str)`
Imports contacts from JSON file with validation.
- **Parameters**: user_id (integer), filename (string)
- **Returns**: 
  - Success: (True, (summary: str, details: dict))
  - Failure: (False, error_message: str)
- **Details dict**: {success, failed, duplicates, errors}

#### `validate_contact_data(contact: dict) -> tuple(bool, str)`
Validates contact JSON data.
- **Parameters**: contact (dict)
- **Returns**: (is_valid: bool, message: str)
- **Checks**: Required fields (name, phone, email), email format

#### `add_history_entry(user_id: int, action: str, file_name: str, count: int, status: str) -> dict`
Records import/export operation.
- **Parameters**: user_id, action ("import"/"export"), file_name, count, status ("success"/"failed")
- **Returns**: History entry dict

#### `get_user_history(user_id: int) -> list`
Gets import/export history for user.
- **Parameters**: user_id (integer)
- **Returns**: List of history entries

---

## Notification Service (`services/notification_service.py`)

### Functions

#### `create_notification(user_id: int, message: str, notification_type: str) -> Notification`
Creates in-system notification.
- **Parameters**: user_id (integer), message (string), notification_type: "system", "birthday", "contact_creation" (string)
- **Returns**: Notification object

#### `get_user_notifications(user_id: int) -> list`
Retrieves all notifications for user.
- **Parameters**: user_id (integer)
- **Returns**: List of notification dictionaries

#### `get_unread_notifications(user_id: int) -> list`
Gets unread notifications only.
- **Parameters**: user_id (integer)
- **Returns**: List of unread notification dicts

#### `mark_notification_as_read(notification_id: int) -> bool`
Marks single notification as read.
- **Parameters**: notification_id (integer)
- **Returns**: True if successful, False otherwise

#### `mark_all_notifications_as_read(user_id: int) -> None`
Marks all user notifications as read.
- **Parameters**: user_id (integer)
- **Returns**: None

#### `send_email(recipient_email: str, subject: str, body: str) -> bool`
Sends email notification (demo mode outputs to console).
- **Parameters**: recipient_email, subject, body (strings)
- **Returns**: True if successful

#### `notify_contact_creation(user_id: int, user_email: str, contact_name: str) -> None`
Sends contact creation notification.
- **Parameters**: user_id (integer), user_email (string), contact_name (string)
- **Returns**: None

#### `notify_birthday(user_id: int, user_email: str, contact_name: str, birthday: str) -> None`
Sends birthday notification.
- **Parameters**: user_id (integer), user_email (string), contact_name (string), birthday (string)
- **Returns**: None

#### `check_birthdays(user_id: int, user_email: str) -> None`
Checks for and sends birthday notifications.
- **Parameters**: user_id (integer), user_email (string)
- **Returns**: None

#### `delete_notification(notification_id: int) -> bool`
Deletes notification.
- **Parameters**: notification_id (integer)
- **Returns**: True if deleted, False otherwise

#### `clear_user_notifications(user_id: int) -> None`
Clears all notifications for user.
- **Parameters**: user_id (integer)
- **Returns**: None

---

## User Service (`services/user_service.py`)

### Functions

#### `get_user_by_id(user_id: int) -> dict | None`
Retrieves user by ID.
- **Parameters**: user_id (integer)
- **Returns**: User dict or None

#### `get_user_by_email(email: str) -> dict | None`
Retrieves user by email.
- **Parameters**: email (string)
- **Returns**: User dict or None

#### `update_user_profile(user_id: int, full_name=None, phone=None, email=None) -> tuple(bool, str)`
Updates user profile information.
- **Parameters**: user_id (integer), optional fields to update
- **Returns**: (success: bool, message: str)
- **Example**: `update_user_profile(user_id, full_name="New Name")`

#### `get_all_users() -> list`
Retrieves all users.
- **Parameters**: None
- **Returns**: List of all user dicts

---

## Data Models

### User Model
```json
{
  "user_id": 1,
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234",
  "password": "hashed_password",
  "created_at": "2026-01-27T10:00:00"
}
```

### Contact Model
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

### Group Model
```json
{
  "group_id": 1,
  "name": "Friends",
  "owner_id": 1,
  "created_at": "2026-01-27T10:00:00"
}
```

### Notification Model
```json
{
  "notification_id": 1,
  "user_id": 1,
  "message": "Contact created successfully",
  "notification_type": "contact_creation",
  "created_at": "2026-01-27T10:00:00",
  "is_read": false
}
```

---

## Error Codes and Messages

| Code | Message | Cause |
|------|---------|-------|
| 1001 | Invalid email format | Email doesn't match pattern |
| 1002 | Email already registered | Duplicate email |
| 1003 | Password must be at least 6 characters | Short password |
| 1004 | User not found | No user with that email/ID |
| 1005 | Invalid email or password | Login failed |
| 2001 | Contact not found | No contact with that ID |
| 2002 | No contacts available | User has no contacts |
| 3001 | Group not found | No group with that name |
| 3002 | Group already exists | Duplicate group name |
| 3003 | Contact already in group | Contact already assigned |
| 4001 | Invalid file format | File is not valid JSON |
| 4002 | File not found | Import file doesn't exist |
| 4003 | Invalid JSON file | Malformed JSON |

---

## Usage Examples

### Complete User Workflow
```python
from services.auth_service import register, login
from services.contact_service import add_contact, search_contacts
from services.group_service import add_group, add_contact_to_group

# Register user
success, msg = register("John Doe", "john@example.com", "555-1234", "password123")

# Login
success, user = login("john@example.com", "password123")
user_id = user['user_id']

# Add contact
contact = add_contact("Jane Smith", "555-5678", "jane@example.com", user_id)

# Create group
group = add_group("Friends", user_id)

# Add contact to group
add_contact_to_group(contact.contact_id, "Friends", user_id)

# Search
results = search_contacts(user_id, "Smith", "name")
```

### Import/Export Workflow
```python
from services.contact_service import view_contacts
from services.import_export_service import export_contacts, import_contacts

# Export
contacts = view_contacts(user_id)
export_contacts(contacts, "backup.json")

# Import
success, result = import_contacts(user_id, "new_contacts.json")
if success:
    summary, details = result
    print(f"Imported: {details['success']}")
    print(f"Duplicates: {details['duplicates']}")
```

---

## Dependencies

- Python 3.12+
- Standard library only (json, os, re, hashlib, datetime, smtplib)

---

**Document Version**: 1.0  
**Last Updated**: January 27, 2026
