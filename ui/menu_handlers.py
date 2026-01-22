from ui.console_utils import print_header, pause, show_message
from services.user_service import create_user, find_user


def main_menu():
    while True:
        print_header("Phone Book Management System")
        print("1. Create user")
        print("2. Find user")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_user_menu()
        elif choice == "2":
            find_user_menu()
        elif choice == "0":
            break
        else:
            show_message("Invalid choice")
            pause()


def create_user_menu():
    print_header("Create User")
    username = input("Username: ")
    password = input("Password: ")

    if find_user(username):
        show_message("User already exists")
    else:
        create_user(username, password)
        show_message("User created successfully")

    pause()


def find_user_menu():
    print_header("Find User")
    username = input("Enter username: ")
    user = find_user(username)

    if user:
        show_message(f"Username: {user['username']} | Role: {user['role']}")
    else:
        show_message("User not found")

    pause()
