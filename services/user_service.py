import json
import os

DATA_FILE = "data/users.json"


def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def create_user(username, password, role="user"):
    users = load_users()
    users.append({
        "username": username,
        "password": password,
        "role": role
    })
    save_users(users)


def find_user(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None
