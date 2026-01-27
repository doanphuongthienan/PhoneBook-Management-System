import json
import os
from datetime import datetime
from services.contact_service import load as load_contacts, add_contact as add_contact_service, check_duplicate

HISTORY_FILE = "data/import_export_history.json"


def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def add_history_entry(user_id, action, file_name, count, status):
    """Add entry to import/export history"""
    history = load_history()
    entry = {
        "id": len(history) + 1,
        "user_id": user_id,
        "action": action,  # import or export
        "file_name": file_name,
        "count": count,
        "status": status,  # success or failed
        "timestamp": datetime.now().isoformat()
    }
    history.append(entry)
    save_history(history)
    return entry


def export_contacts(contacts, filename):
    """Export contacts to JSON file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
        return True, f"Exported {len(contacts)} contacts to {filename}"
    except Exception as e:
        return False, f"Export failed: {e}"


def export_contacts_by_group(user_id, group_name, filename):
    """Export contacts from a specific group"""
    from services.contact_service import get_contacts_by_group
    
    contacts = get_contacts_by_group(user_id, group_name)
    if not contacts:
        return False, "No contacts found in this group"
    
    return export_contacts(contacts, filename)


def validate_contact_data(contact):
    """Validate contact data before import"""
    required_fields = ["name", "phone", "email"]
    for field in required_fields:
        if not contact.get(field):
            return False, f"Missing required field: {field}"
    
    # Validate email format
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, contact.get("email", "")):
        return False, "Invalid email format"
    
    return True, "Valid"


def import_contacts(user_id, filename):
    """Import contacts from JSON file with validation and duplicate checking"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            imported_data = json.load(f)
        
        if not isinstance(imported_data, list):
            return False, "Invalid file format. Expected array of contacts."
        
        successful_imports = 0
        failed_imports = 0
        duplicate_count = 0
        errors = []
        
        for idx, contact in enumerate(imported_data, 1):
            # Validate contact data
            is_valid, msg = validate_contact_data(contact)
            if not is_valid:
                errors.append(f"Row {idx}: {msg}")
                failed_imports += 1
                continue
            
            # Check for duplicates
            if check_duplicate(user_id, contact.get("phone"), contact.get("email")):
                duplicate_count += 1
                continue
            
            # Add contact
            try:
                add_contact_service(
                    contact.get("name"),
                    contact.get("phone"),
                    contact.get("email"),
                    user_id,
                    contact.get("address", ""),
                    contact.get("notes", ""),
                    contact.get("birthday"),
                    contact.get("groups", [])
                )
                successful_imports += 1
            except Exception as e:
                errors.append(f"Row {idx}: {e}")
                failed_imports += 1
        
        summary = f"Import completed: {successful_imports} imported"
        if duplicate_count > 0:
            summary += f", {duplicate_count} duplicates skipped"
        if failed_imports > 0:
            summary += f", {failed_imports} failed"
        
        result = {
            "success": successful_imports,
            "failed": failed_imports,
            "duplicates": duplicate_count,
            "errors": errors
        }
        
        return True, (summary, result)
    
    except json.JSONDecodeError:
        return False, "Invalid JSON file"
    except FileNotFoundError:
        return False, f"File not found: {filename}"
    except Exception as e:
        return False, f"Import failed: {e}"


def get_user_history(user_id):
    """Get import/export history for a user"""
    history = load_history()
    return [h for h in history if h["user_id"] == user_id]


def get_all_history():
    """Get all import/export history"""
    return load_history()

