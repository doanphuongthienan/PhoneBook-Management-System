import json
import os
from models.user_model import User

DATA_FILE = "data/users.json"


def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def get_user_by_id(user_id):
    """Get user by ID"""
    users = load_users()
    for u in users:
        if u.get("user_id") == user_id:
            return u
    return None


def get_user_by_email(email):
    """Get user by email"""
    users = load_users()
    for u in users:
        if u.get("email") == email:
            return u
    return None


def update_user_profile(user_id, full_name=None, phone=None, email=None):
    """Update user profile information"""
    users = load_users()
    for u in users:
        if u.get("user_id") == user_id:
            if full_name:
                u["full_name"] = full_name
            if phone:
                u["phone"] = phone
            if email:
                # Check if email already exists
                if any(user.get("email") == email and user.get("user_id") != user_id for user in users):
                    return False, "Email already in use"
                u["email"] = email
            save_users(users)
            return True, "Profile updated successfully"
    return False, "User not found"


def get_all_users():
    """Get all users"""
    return load_users()


def find_user(username):
    """Legacy: Find user by username - kept for compatibility"""
    users = load_users()
    for user in users:
        if user.get("full_name") == username or user.get("email") == username:
            return user
    return None


def create_user(full_name, email, phone, password):
    """Legacy: Create user - kept for compatibility"""
    users = load_users()
    user_id = len(users) + 1
    new_user = {
        "user_id": user_id,
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "password": password,
        "created_at": __import__('datetime').datetime.now().isoformat()
    }
    users.append(new_user)
    save_users(users)
    return new_user

