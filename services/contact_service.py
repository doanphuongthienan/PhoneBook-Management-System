import json
import os
from datetime import datetime
from models.contact_model import Contact

DATA = "data/contacts.json"


def load():
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save(data):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_contact(name, phone, email, owner_id, address="", notes="", birthday=None, groups=None):
    """Add a new contact"""
    contacts = load()
    contact_id = len(contacts) + 1
    
    c = Contact(contact_id, name, phone, email, owner_id, address, notes, birthday, groups or [])
    contacts.append(c.to_dict())
    save(contacts)
    
    return c


def view_contacts(owner_id):
    """View all contacts for a user"""
    return [c for c in load() if c["owner_id"] == owner_id]


def get_contact_by_id(contact_id, owner_id):
    """Get specific contact details"""
    contacts = load()
    for c in contacts:
        if c["contact_id"] == contact_id and c["owner_id"] == owner_id:
            return c
    return None


def search_contacts(owner_id, keyword, search_type="all"):
    """
    Search contacts with multiple criteria
    search_type: 'all', 'name', 'phone', 'email', 'group'
    """
    contacts = load()
    keyword = keyword.lower()
    results = []
    
    for c in contacts:
        if c["owner_id"] != owner_id:
            continue
            
        if search_type == "all":
            if (keyword in c.get("name", "").lower() or
                keyword in c.get("phone", "").lower() or
                keyword in c.get("email", "").lower() or
                any(keyword in g.lower() for g in c.get("groups", []))):
                results.append(c)
        elif search_type == "name":
            if keyword in c.get("name", "").lower():
                results.append(c)
        elif search_type == "phone":
            if keyword in c.get("phone", "").lower():
                results.append(c)
        elif search_type == "email":
            if keyword in c.get("email", "").lower():
                results.append(c)
        elif search_type == "group":
            if any(keyword in g.lower() for g in c.get("groups", [])):
                results.append(c)
    
    return results


def sort_contacts(contacts, sort_by="name", ascending=True):
    """Sort contacts by name, created_at, or group"""
    if sort_by == "name":
        return sorted(contacts, key=lambda x: x.get("name", "").lower(), reverse=not ascending)
    elif sort_by == "created_at":
        return sorted(contacts, key=lambda x: x.get("created_at", ""), reverse=not ascending)
    elif sort_by == "group":
        return sorted(contacts, key=lambda x: ", ".join(x.get("groups", [])).lower(), reverse=not ascending)
    return contacts


def edit_contact(contact_id, owner_id, **kwargs):
    """Edit existing contact information"""
    contacts = load()
    for c in contacts:
        if c["contact_id"] == contact_id and c["owner_id"] == owner_id:
            # Update allowed fields
            allowed_fields = ["name", "phone", "email", "address", "notes", "birthday", "groups"]
            for field in allowed_fields:
                if field in kwargs and kwargs[field] is not None:
                    c[field] = kwargs[field]
            c["updated_at"] = datetime.now().isoformat()
            save(contacts)
            return True, "Contact updated successfully"
    
    return False, "Contact not found"


def delete_contact(contact_id, owner_id):
    """Delete a contact with confirmation"""
    contacts = load()
    original_len = len(contacts)
    contacts = [c for c in contacts if not (c["contact_id"] == contact_id and c["owner_id"] == owner_id)]
    
    if len(contacts) < original_len:
        save(contacts)
        return True, "Contact deleted successfully"
    return False, "Contact not found"


def get_contacts_by_group(owner_id, group_name):
    """Get all contacts in a specific group"""
    contacts = load()
    return [c for c in contacts if c["owner_id"] == owner_id and group_name in c.get("groups", [])]


def check_duplicate(owner_id, phone, email):
    """Check for duplicate contacts (same phone or email)"""
    contacts = load()
    for c in contacts:
        if c["owner_id"] == owner_id:
            if c.get("phone") == phone or c.get("email") == email:
                return True
    return False

