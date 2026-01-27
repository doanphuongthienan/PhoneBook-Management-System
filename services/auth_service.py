import json
import re
import hashlib
from datetime import datetime
from models.user_model import User

DATA = "data/users.json"


def load_users():
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_users(users):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password meets minimum security requirements"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Valid"


def email_exists(email):
    """Check if email already registered"""
    users = load_users()
    return any(u.get("email") == email for u in users)


def register(full_name, email, phone, password):
    """Register a new user account"""
    # Validate email format
    if not validate_email(email):
        return False, "Invalid email format"
    
    # Check if email already exists
    if email_exists(email):
        return False, "Email already registered"
    
    # Validate password
    is_valid, msg = validate_password(password)
    if not is_valid:
        return False, msg
    
    # Create new user
    users = load_users()
    user_id = len(users) + 1
    hashed_password = hash_password(password)
    
    user = User(user_id, full_name, email, phone, hashed_password)
    users.append(user.to_dict())
    save_users(users)
    
    return True, "Registration successful"


def login(email, password):
    """Login user with email and password"""
    users = load_users()
    for u in users:
        if u.get("email") == email and verify_password(password, u.get("password", "")):
            return True, u
    return False, None


def get_user_by_email(email):
    """Get user by email"""
    users = load_users()
    for u in users:
        if u.get("email") == email:
            return u
    return None


def reset_password(email, new_password):
    """Reset user password"""
    is_valid, msg = validate_password(new_password)
    if not is_valid:
        return False, msg
    
    users = load_users()
    for u in users:
        if u.get("email") == email:
            u["password"] = hash_password(new_password)
            save_users(users)
            return True, "Password reset successful"
    
    return False, "Email not found"

