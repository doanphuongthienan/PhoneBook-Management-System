def clear_screen():
    print("\n" * 50)


def pause():
    input("Press Enter to continue...")


def print_header(title):
    clear_screen()
    print("=" * 40)
    print(title.upper())
    print("=" * 40)


def show_message(message):
    print(message)
