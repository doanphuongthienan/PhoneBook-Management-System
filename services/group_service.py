import json
import os
from models.group_model import Group

DATA = "data/groups.json"


def load():
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save(data):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_group(name, owner_id):
    """Add a new contact group"""
    groups = load()
    group_id = len(groups) + 1
    g = Group(group_id, name, owner_id)
    groups.append(g.to_dict())
    save(groups)
    return g


def get_user_groups(owner_id):
    """Get all groups for a user"""
    groups = load()
    return [g for g in groups if g["owner_id"] == owner_id]


def get_group_by_id(group_id, owner_id):
    """Get specific group"""
    groups = load()
    for g in groups:
        if g["group_id"] == group_id and g["owner_id"] == owner_id:
            return g
    return None


def get_group_by_name(name, owner_id):
    """Get group by name"""
    groups = load()
    for g in groups:
        if g.get("name", "").lower() == name.lower() and g["owner_id"] == owner_id:
            return g
    return None


def group_exists(name, owner_id):
    """Check if group already exists"""
    groups = load()
    return any(g.get("name", "").lower() == name.lower() and g["owner_id"] == owner_id for g in groups)


def delete_group(group_id, owner_id):
    """Delete a group"""
    groups = load()
    original_len = len(groups)
    groups = [g for g in groups if not (g["group_id"] == group_id and g["owner_id"] == owner_id)]
    
    if len(groups) < original_len:
        save(groups)
        return True, "Group deleted successfully"
    return False, "Group not found"


def rename_group(group_id, owner_id, new_name):
    """Rename a group"""
    groups = load()
    for g in groups:
        if g["group_id"] == group_id and g["owner_id"] == owner_id:
            # Check if new name already exists
            if group_exists(new_name, owner_id):
                return False, "Group name already exists"
            g["name"] = new_name
            save(groups)
            return True, "Group renamed successfully"
    return False, "Group not found"


def add_contact_to_group(contact_id, group_name, owner_id):
    """Add a contact to a group through contact service"""
    from services.contact_service import load as load_contacts, save as save_contacts
    
    contacts = load_contacts()
    group_exists_flag = group_exists(group_name, owner_id)
    
    if not group_exists_flag:
        return False, "Group does not exist"
    
    for c in contacts:
        if c["contact_id"] == contact_id and c["owner_id"] == owner_id:
            if group_name not in c.get("groups", []):
                c["groups"].append(group_name)
                save_contacts(contacts)
                return True, f"Contact added to group '{group_name}'"
            else:
                return False, "Contact already in this group"
    
    return False, "Contact not found"


def remove_contact_from_group(contact_id, group_name, owner_id):
    """Remove a contact from a group"""
    from services.contact_service import load as load_contacts, save as save_contacts
    
    contacts = load_contacts()
    
    for c in contacts:
        if c["contact_id"] == contact_id and c["owner_id"] == owner_id:
            if group_name in c.get("groups", []):
                c["groups"].remove(group_name)
                save_contacts(contacts)
                return True, f"Contact removed from group '{group_name}'"
            else:
                return False, "Contact not in this group"
    
    return False, "Contact not found"

