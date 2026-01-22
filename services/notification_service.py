import datetime


def create_notification(message):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "message": message,
        "time": time
    }


def show_notification(notification):
    print(f"[{notification['time']}] {notification['message']}")
