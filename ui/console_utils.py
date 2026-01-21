def clear_screen():
    print("\n" * 50)


def pause():
    input("Nhấn Enter để tiếp tục...")


def print_header(title):
    clear_screen()
    print("=" * 40)
    print(title.upper())
    print("=" * 40)


def show_message(message):
    print(message)
